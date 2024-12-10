import ffmpegcv
import sys

# Input and output file paths
input_file = sys.argv[1]
output_file = sys.argv[2]

# Initialize video reader and writer
reader = ffmpegcv.VideoReader(input_file)
writer = ffmpegcv.VideoWriter(
    output_file,
    fps=reader.fps,
    codec='h264',
    pix_fmt='yuv420p'
    )

framenum= 0
# Process video frame by frame
for frame in reader:
    # Process frame if needed (e.g., apply filters, transformations, etc.)
    processed_frame = frame  # For now, we simply copy the frame
    framenum += 1
    print(framenum)
    # Write the frame to the output video
    writer.write(processed_frame)

# Release resources
reader.release()
writer.release()

print(f"Video copied successfully to {output_file}")
