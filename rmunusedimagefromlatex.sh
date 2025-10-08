#!/bin/bash
# remove-unused-images.sh
# Usage: ./remove-unused-images.sh tee.tex images/ [--delete]

TEXFILE="$1"
IMGDIR="$2"
DELETE="$3"   # pass --delete to actually remove

# 1. Extract image filenames directly from inside { ... }
used=$(grep -oP '\\includegraphics(?:\[[^]]*\])?{\K[^}]+' "$TEXFILE")

# 2. Build a list of used images (with and without extensions)
declare -A keep
for f in $used; do
    base=$(basename "$f")    # strip path if any
    # If extension is present, keep it directly
    if [[ "$base" == *.* ]]; then
        keep["$base"]=1
    else
        # no extension → allow jpg, jpeg, png, 
        for ext in jpg jpeg png tiff tif; do
            keep["$base.$ext"]=1
        done
    fi
done

# 3. Go through all image files in the folder
shopt -s nullglob
for file in "$IMGDIR"/*.{jpg,jpeg,png,tif,tiff}; do
    fname=$(basename "$file")
    if [ -z "${keep[$fname]}" ]; then
        if [ "$DELETE" == "--delete" ]; then
            echo "Deleting unused: $fname"
            rm "$file"
        else
            echo "Would delete: $fname"
        fi
    fi
done
shopt -u nullglob
