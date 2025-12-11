import requests
import folium
import json
import pandas as pd

def get_schools_data_from_osm():
    """
    Queries the Overpass API for schools in the Cilacap area and returns
    a list of dictionaries containing school data (name, lat, lon).
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Overpass QL Query: Find nodes, ways, and relations tagged as school in "Cilacap"
    # We use 'out center;' to get a center point for ways and relations as well.
    overpass_query = """
    [out:json][timeout:60];
    area[name="Cilacap"]->.searchArea;
    (
      nwr["amenity"="school"](area.searchArea);
    );
    out center;
    """

    print("Sending query to Overpass API for schools in Cilacap...")
    
    try:
        response = requests.post(overpass_url, data={'data': overpass_query})
        response.raise_for_status()
        data = response.json()
        
        schools_list = []
        
        for element in data['elements']:
            tags = element.get('tags', {})
            name = tags.get('name', 'N/A')
            
            lat, lon = None, None
            
            # Get coordinates based on element type
            if element.get('type') == 'node':
                lat = element.get('lat')
                lon = element.get('lon')
            elif element.get('type') in ('way', 'relation') and 'center' in element:
                lat = element['center'].get('lat')
                lon = element['center'].get('lon')
            
            # Only include elements with valid coordinates and a name tag
            if lat is not None and lon is not None and name != 'N/A':
                schools_list.append({
                    'name': name,
                    'lat': lat,
                    'lon': lon
                })
        
        print(f"✅ Query successful. Found {len(schools_list)} schools with name and coordinates.")
        return schools_list
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while connecting to the API: {e}")
        return []

def create_folium_map(schools_data):
    """
    Creates an interactive Folium map with markers for each school.
    """
    if not schools_data:
        print("No school data to map.")
        return None

    # Calculate the mean center point for initial map view (approx. center of Cilacap)
    # Defaulting to a central point if data is sparse.
    if schools_data:
        df = pd.DataFrame(schools_data)
        avg_lat = df['lat'].mean()
        avg_lon = df['lon'].mean()
    else:
        # Fallback coordinates for Cilacap
        avg_lat = -7.65
        avg_lon = 109.02

    # Initialize the map centered on the calculated or default location
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

    # Add markers for each school
    # for school in schools_data:
        # Create a marker with a nice school icon
        # folium.Marker(
        #     location=[school['lat'], school['lon']],
        #     popup=f"<b>{school['name']}</b>", # Display school name on click
        #     tooltip=school['name'],
        #     icon=folium.Icon(color='blue', icon='graduation-cap', prefix='fa')
        # ).add_to(m)

    print("\n🗺️ Map created successfully.")
    return m

# --- Execution ---
if __name__ == "__main__":
    # 1. Get the school data
    schools = get_schools_data_from_osm()
    
    # 2. Create the Folium map
    cilacap_map = create_folium_map(schools)
    
    # 3. Save the map to an HTML file
    if cilacap_map:
        file_name = "cilacap_schools.html"
        cilacap_map.save(file_name)
        print(f"The interactive map has been saved to '{file_name}'. Open this file in your web browser to view the map.")