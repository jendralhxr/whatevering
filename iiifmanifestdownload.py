import json
import os
import ssl
import urllib.request

# Create an unverified SSL context to bypass local certificate errors
ssl_context = ssl._create_unverified_context()


def download_from_manifest_file(
    json_file_path, output_dir="downloaded_images"
):
    os.makedirs(output_dir, exist_ok=True)

    with open(json_file_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # IIIF v3 canvas list
    canvases = manifest.get("items", [])
    print(f"Found {len(canvases)} pages in manifest. Starting download...\n")

    for idx, canvas in enumerate(canvases, start=1):
        try:
            # Extract label if available
            label_dict = canvas.get("label", {})
            label = (
                label_dict.get("none", [f"page_{idx:02d}"])[0]
                if "none" in label_dict
                else f"page_{idx:02d}"
            )

            # Traverse IIIF v3 structure: items -> items -> body
            anno_pages = canvas.get("items", [])
            if not anno_pages:
                continue

            annotations = anno_pages[0].get("items", [])
            if not annotations:
                continue

            body = annotations[0].get("body", {})

            # Get the IIIF image service ID or base ID
            service = body.get("service", [])
            if service:
                service_id = service[0].get("id")
                # Construct IIIF full-resolution URL
                img_url = f"{service_id}/full/full/0/default.jpg"
            else:
                img_url = body.get("id")

            # Clean label for file path
            safe_label = "".join(
                c if c.isalnum() or c in (" ", "-", "_") else "_" for c in label
            )
            file_name = f"{idx:02d}_{safe_label}.jpg"
            file_path = os.path.join(output_dir, file_name)

            print(f"[{idx}/{len(canvases)}] Downloading {file_name}...")

            # Download full resolution image
            req = urllib.request.Request(
                img_url, headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(
                req, context=ssl_context
            ) as response, open(file_path, "wb") as f_out:
                f_out.write(response.read())

        except Exception as e:
            print(f"Failed to download item {idx}: {e}")

    print("\nAll downloads finished!")


if __name__ == "__main__":
    download_from_manifest_file("manifest.json")