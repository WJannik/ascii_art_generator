import cv2
import numpy as np
import os
from tqdm import tqdm
from ascii_art_generator_image import generate_ascii_art

def convert_frame_to_ascii(frame, temp_frame_path, temp_ascii_path, num_sub_images_x=100):
    """
    Convert a single video frame to ASCII art using the existing generate_ascii_art function.
    
    Args:
        frame: Input video frame (BGR)
        temp_frame_path: Path to save temporary frame
        temp_ascii_path: Path to save temporary ASCII result
        num_sub_images_x: Number of sub-images in x dimension (controls resolution)
        
    Returns:
        ASCII art frame as grayscale image
    """
    # Save frame temporarily
    cv2.imwrite(temp_frame_path, frame)
    
    # Generate ASCII art using existing function
    ascii_art = generate_ascii_art(
        image_path=temp_frame_path,
        ascii_images_dir='ascii_images',
        num_sub_images_x=num_sub_images_x,
        output_path=temp_ascii_path,
        plot_enabled=False,
        save_enabled=False
    )
    
    return ascii_art

# Configuration
mp4_path = r"c:\Users\janni\OneDrive\VID_20250514_183114.mp4"
output_path = r"c:\Users\janni\OneDrive\VID_20250514_183114_ascii.mp4"
ascii_images_dir = "ascii_images"  # Directory containing ASCII character images

# ASCII art parameters
num_sub_images_x = 100  # Lower values = more pixelated, higher values = more detailed

# Open the video file
cap = cv2.VideoCapture(mp4_path)

start_time = 0.0  # in seconds
end_time = 12.0 # in seconds

# Speed multiplier: 1.0 = normal speed, 2.0 = 2x speed, 0.5 = slow motion
speed_multiplier = 1.0

# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
else:
    print("Video file opened successfully!")
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Video properties: {width}x{height} @ {fps} fps, {total_frames} frames")
    print(f"Speed multiplier: {speed_multiplier}x")
    
    # Create temporary file paths for frame processing
    temp_frame_path = "temp_frame.jpg"
    temp_ascii_path = "temp_ascii.png"
    
    # Calculate start and end frame numbers
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    
    print(f"Converting frames {start_frame} to {end_frame} ({start_time}s - {end_time}s) to ASCII art")
    
    # Set the video to start at the start_frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    # Define the codec and create VideoWriter object
    # For ASCII art, we'll use grayscale output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=False)
    
    frame_count = start_frame
    frames_written = 0
    
    # Process each frame with progress bar
    print("Processing video frames to ASCII art...")
    progress_bar = tqdm(total=end_frame-start_frame, desc="Converting frames", unit="frames")
    
    while frame_count <= end_frame:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Skip frames based on speed multiplier to reduce file size
        # For 2x speed, only process every 2nd frame
        if (frame_count - start_frame) % int(speed_multiplier) != 0:
            frame_count += 1
            progress_bar.update(1)
            continue
        
        # Convert frame to ASCII art
        ascii_frame = convert_frame_to_ascii(
            frame, 
            temp_frame_path,
            temp_ascii_path,
            num_sub_images_x
        )

        # Write the ASCII frame to output video
        out.write(ascii_frame)
        frames_written += 1
        
        frame_count += 1
        progress_bar.update(1)
    
    progress_bar.close()
    
    original_duration = (end_frame - start_frame) / fps
    new_duration = frames_written / fps
    
    print(f"ASCII video conversion complete!")
    print(f"Written {frames_written} ASCII frames to: {output_path}")
    print(f"Original duration: {original_duration:.2f}s, New duration: {new_duration:.2f}s")
    
    # Release resources
    cap.release()
    out.release()
    
    # Clean up temporary files
    if os.path.exists(temp_frame_path):
        os.remove(temp_frame_path)
    if os.path.exists(temp_ascii_path):
        os.remove(temp_ascii_path)
    
    print("Done! Your ASCII art video is ready!")