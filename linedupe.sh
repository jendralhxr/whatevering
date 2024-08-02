#!/bin/bash

# Check if the file argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 filename"
    exit 1
fi

filename=$1

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File not found!"
    exit 1
fi

# Find and print duplicate lines with their line numbers
echo "Duplicate lines in $filename with line numbers:"

# Number the lines, sort them, find duplicates, and then match them with the original lines to get line numbers
nl -b a "$filename" | sort -k2 | uniq -Df1 | awk '{print $2}' | while read -r line; do
    grep -nFx "$line" "$filename"
done
