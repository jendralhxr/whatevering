#!/bin/bash

# Check if the user provided a directory argument
if [ -z "$1" ]; then
  echo "Usage: $0 /path_to_your_directory"
  exit 1
fi

# Navigate to the specified directory
directory="$1"
cd "$directory" || { echo "Directory not found: $directory"; exit 1; }

# Loop through all png files
for file in *.jpg; do
  # Extract the numeric part of the filename (before the .png extension)
  base=$(basename "$file" .jpg)
  
  # Pad the number with zeros to 4 digits (adjust 4 to the desired length)
  new_base=$(printf "%04d" "$base")
  
  # Rename the file with padded zeros
  mv "$file" "${new_base}.jpg"
done

echo "Files have been renamed successfully!"
