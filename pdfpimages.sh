#!/usr/bin/bash
mkdir -p "$1" && pdfimages -p -j "$2" "$1/tmp" && i=0; for img in "$1"/tmp-*; do [[ -f "$img" ]] || continue; p=$(basename "$img" | cut -d'-' -f2 | sed 's/^0*//'); printf -v pp "%03d" "$p"; printf -v nn "%03d" "$((i++))"; convert "$img" "$1/$pp-$nn.jpg"; done
