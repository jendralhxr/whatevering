#!/usr/bin/env python3
import sys
import pikepdf

input_file = "temp.pdf"
output_file = "output.pdf"

# Open PDF
pdf = pikepdf.open(input_file)

# The replacements
old_emails = [
    "meme1@gmail.com",
    "meme2@gmail.com",
    "meme3@gmail.com"
]
new_email = "gege@gogo.ac.id"

# Iterate through page contents
for page in pdf.pages:
    if "/Contents" in page:
        contents = page.Contents.read_bytes().decode("latin-1")  # raw text
        for old in old_emails:
            contents = contents.replace(old, new_email)
        page.Contents.stream = contents.encode("latin-1")

# Save to new file
pdf.save(output_file)
