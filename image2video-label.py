import cv2
import os
import sys
import re
PHI= 1.6180339887498948482 # ppl says this is a beautiful number :)


def create_video_from_images(directory, output_video_file, fps=20):
    # Ensure the directory exists
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    # Get list of JPG files in the directory
    images = [img for img in os.listdir(directory) if img.lower().endswith(".png")]
    images.sort()  # Ensure images are processed in the correct order

    if not images:
        print("No images found in the directory.")
        return

    # Read the first image to get the size
    first_image_path = os.path.join(directory, images[0])
    frame = cv2.imread(first_image_path)
    if frame is None:
        print(f"Error: Unable to read the image '{first_image_path}'.")
        return
    
    height, width, _ = frame.shape

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
    video_writer = cv2.VideoWriter(output_video_file, fourcc, fps, (width, height))

    if not video_writer.isOpened():
        print(f"Error: Unable to open video file '{output_video_file}' for writing.")
        return

    # Write each image to the video file
    for image in images:
        image_path = os.path.join(directory, image)
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"Warning: Unable to read the image '{image_path}'. Skipping.")
            continue

        imagename, ext= os.path.splitext(image_path)
        match = re.search(r'\d+', imagename)
        if match:
            freq= int(match.group())
        #freq= int(imagename)
        print(f"{imagename} {freq}")
        #cv2.putText(frame, f"{freq} Hz", (int(width/PHI), int(height/PHI)), cv2.FONT_HERSHEY_SIMPLEX, 8, (0, 0, 200), 4)
        cv2.putText(frame, sys.argv[3], (int(width*0.1), int(height*0.1)), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 200), 4)
        
        
        video_writer.write(frame)

    # Release the video writer
    video_writer.release()
    print(f"Video saved as {output_video_file}")

# Usage
input_directory = sys.argv[1]  # Replace with the path to your directory
output_file = sys.argv[2]  # Output video file name
create_video_from_images(input_directory, output_file, fps=6)
