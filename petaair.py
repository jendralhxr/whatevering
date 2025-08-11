# surabaya_water_distance_map.py
import osmnx as ox
import geopandas as gpd
import numpy as np
from rasterio import features
from shapely.ops import unary_union
from scipy import ndimage
import matplotlib.pyplot as plt
import folium
from folium.raster_layers import ImageOverlay
from branca.colormap import LinearColormap
from PIL import Image
import io
import pandas as pd

# -------------- Parameters --------------
PLACE = "Surabaya, Indonesia"
# raster resolution in meters per pixel
RESOLUTION_M = 10.0
# distance cutoff (meters) -> value 0 at >= this distance
CUTOFF_M = 400.0
# colormap name (matplotlib)
CMAP = "viridis"
# output temporary image size scale (controls image quality)
PNG_DPI = 150
# ----------------------------------------

# 1. download water geometries from OSM
tags = {
    "natural": ["water"],
    "water": True,                       # ponds, lakes, etc.
    "waterway": ["river", "stream", "canal", "drain"]
}
print("Downloading water features from OSM...")
gdfs = []
# osmnx.features_from_place accepts dict of tags; we'll call once per key pair to be safe
# (some OSM tags mix types; this approach collects a broad set)
gdfs.append(ox.features_from_place(PLACE, {"natural":"water"}))
gdfs.append(ox.features_from_place(PLACE, {"natural":"wetland"}))
gdfs.append(ox.features_from_place(PLACE, {"water": True}))
gdfs.append(ox.features_from_place(PLACE, {"waterway": ["river","stream","canal","drain"]}))
gdfs.append(ox.features_from_place(PLACE, {"leisure":"swimming_pool"}))


# combine and only keep geometry column
water_gdf = gpd.GeoDataFrame(pd.concat([gdf[['geometry']] for gdf in gdfs], ignore_index=True))
water_gdf = water_gdf[~water_gdf.geometry.is_empty].dropna(how="all")
water_gdf = water_gdf.set_geometry('geometry')
water_gdf.crs = gdfs[0].crs  # they should share same CRS (EPSG:4326)
water_gdf = water_gdf.to_crs(epsg=3857)  # project to meters (WebMercator)

if len(water_gdf) == 0:
    raise RuntimeError("No water features found for the place. Check network or place name.")

# 2. merge geometry into single unary_union
print("Merging geometries...")
water_union = unary_union(water_gdf.geometry.values)

# 3. bounding box (with a small buffer)
bounds = water_gdf.total_bounds  # minx, miny, maxx, maxy in EPSG:3857
minx, miny, maxx, maxy = bounds
pad = 2000  # add 2 km pad around collected water features so map extends beyond water
minx -= pad; miny -= pad; maxx += pad; maxy += pad

width_m = maxx - minx
height_m = maxy - miny

# 4. compute raster size
nx = int(np.ceil(width_m / RESOLUTION_M))
ny = int(np.ceil(height_m / RESOLUTION_M))
print(f"Raster size: {nx} x {ny} pixels (resolution {RESOLUTION_M} m)")

# 5. transform (affine) from pixel coords to map coords (rasterio style)
from affine import Affine
transform = Affine.translation(minx, maxy) * Affine.scale(RESOLUTION_M, -RESOLUTION_M)
# note: using origin at top-left: (minx, maxy), scale y negative.

# 6. rasterize water geometries into boolean mask
print("Rasterizing water geometries...")
water_shapes = [(water_union, 1)]
mask = features.rasterize(
    shapes=water_shapes,
    out_shape=(ny, nx),
    transform=transform,
    fill=0,
    dtype=np.uint8
)

# 7. compute distance transform (in pixels) and convert to meters
print("Computing distance transform...")
# distance_transform_edt computes distance to nearest zero pixel; we want dist to water pixels:
# so invert mask: water==1 -> background False; use inverse: non-water True => distance to nearest water
inv_mask = (mask == 0).astype(np.uint8)
dist_pixels = ndimage.distance_transform_edt(inv_mask)  # in pixels
dist_m = dist_pixels * RESOLUTION_M

# 8. convert distance to value in [0,1] where 1 at water (dist=0), 0 at >=CUTOFF_M
print("Converting to normalized values (1 at water, 0 at >=400 m)...")
values = 1.0 - (dist_m / CUTOFF_M)
values = np.clip(values, 0.0, 1.0)

# 9. make RGBA image with matplotlib colormap (alpha for zeros)
print("Rendering overlay image...")
import matplotlib
cmap = matplotlib.cm.get_cmap(CMAP)
# map values to colors
rgba = cmap(values)  # shape (ny, nx, 4), values in 0..1
# make pixels where value==0 transparent
rgba[..., 3] = np.where(values <= 0.0, 0.0, 0.8)  # semi-opaque for visible area
# convert to 8-bit image
rgba_8 = (rgba * 255).astype(np.uint8)
pil_img = Image.fromarray(rgba_8)

# save PNG to bytes
buf = io.BytesIO()
pil_img.save(buf, format="PNG")
buf.seek(0)

# 10. get extent in lat/lon for Folium ImageOverlay (bounds: [[south, west], [north, east]])
# corners in EPSG:3857 -> convert to EPSG:4326 latlon
import pyproj
proj_3857 = pyproj.CRS.from_epsg(3857)
proj_4326 = pyproj.CRS.from_epsg(4326)
transformer = pyproj.Transformer.from_crs(proj_3857, proj_4326, always_xy=True)

# top-left (minx, maxy), bottom-right (maxx, miny)
west, north = transformer.transform(minx, maxy)
east, south = transformer.transform(maxx, miny)
bounds_latlon = [[south, west], [north, east]]

## 11-a
import base64

# Convert PIL Image to PNG bytes
from io import BytesIO
buf = BytesIO()
pil_img.save(buf, format="PNG")
png_data = buf.getvalue()

# Encode as base64 string for folium
b64encoded = base64.b64encode(png_data).decode("utf-8")
img_data_uri = f"data:image/png;base64,{b64encoded}"

# Add overlay
image_overlay = folium.raster_layers.ImageOverlay(
    image=img_data_uri,
    bounds=bounds_latlon,
    name="distance_to_water",
    opacity=0.8,
    interactive=True,
    cross_origin=False,
    zindex=1
)


# 11. create folium map centered on Surabaya
print("Building folium map...")
center_lat, center_lon = transformer.transform((minx + maxx) / 2, (miny + maxy) / 2)[::-1]  # get lat, lon
m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="cartodbpositron")

# add water overlay image
img_bytes = buf.getvalue()
image_overlay = folium.raster_layers.ImageOverlay(
    image=img_data_uri,
    bounds=bounds_latlon,
    name="distance_to_water",
    opacity=0.8,
    interactive=True,
    cross_origin=False,
    zindex=1
)

image_overlay.add_to(m)

# add legend / colorbar
colormap = LinearColormap(
    colors=[matplotlib.colors.to_hex(cmap(i)[:3]) for i in np.linspace(0,1,256)],
    vmin=0.0, vmax=1.0,
    caption="Proximity value (1=water → 0 at >=400 m)"
)
colormap.add_to(m)

# add layer control
folium.LayerControl().add_to(m)

# save map
out_html = "surabaya_water_distance_map.html"
m.save(out_html)
print(f"Saved map to {out_html}. Open it in your browser.")
