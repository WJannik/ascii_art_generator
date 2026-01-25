import cv2
import numpy as np
import os
from tqdm import tqdm

from .ascii_art_generator_image import generate_ascii_art
from .utils_compression import compress_video


def convert_frame_to_ascii(frame, temp_frame_path, temp_ascii_path, num_sub_images_width=100, ascii_images_dir=None):
    """
    Convert a single video frame to ASCII art using the existing generate_ascii_art function.
    
    Args:
        frame: Input video frame (BGR)
        temp_frame_path: Path to save temporary frame
        temp_ascii_path: Path to save temporary ASCII result
        num_sub_images_width: Number of sub-images in x dimension (controls resolution)
        ascii_images_dir: Directory containing ASCII character images
        
    Returns:
        ASCII art frame as grayscale image
    """
    # Set default ascii_images_dir if not provided
    if ascii_images_dir is None:
        current_dir = os.path.dirname(__file__)
        ascii_images_dir = os.path.join(current_dir, 'ascii_images')
    
    # Save frame temporarily
    cv2.imwrite(temp_frame_path, frame)
    
    # Generate ASCII art using existing function
    ascii_art = generate_ascii_art(
        image_path=temp_frame_path,
        ascii_images_dir=ascii_images_dir,
        num_sub_images_width=num_sub_images_width,
        output_path=temp_ascii_path,
        plot_enabled=False,
        save_enabled=False,
        generate_ascii_images_flag=False
    )
    cv2.imwrite(temp_ascii_path, ascii_art)
    return ascii_art

def convert_video_to_ascii(input_video_path, output_video_path, start_time=0.0, end_time=None, 
                          num_sub_images_width=100, speed_multiplier=1.0, ascii_images_dir=None,
                          compress_output=True, compression_level='medium'):
    """
    Convert a video to ASCII art video.
    Args:
        input_video_path (str): Path to the input video file
        output_video_path (str): Path where the ASCII video will be saved
        start_time (float): Start time in seconds (default: 0.0)
        end_time (float): End time in seconds (default: None - full video)
        num_sub_images_width (int): ASCII resolution - lower = more pixelated, higher = more detailed (default: 100)
        speed_multiplier (float): Speed multiplier - 1.0 = normal, 2.0 = 2x speed, 0.5 = slow motion (default: 1.0)
        ascii_images_dir (str): Directory containing ASCII character images (default: package ascii_images)
        compress_output (bool): Whether to compress the output video to reduce file size (default: True)
        compression_level (str): Compression level - 'low', 'medium', 'high' (default: 'medium')
    Returns:
        bool: True if successful, False otherwise
    """
    
    # Set default ascii_images_dir if not provided
    if ascii_images_dir is None:
        current_dir = os.path.dirname(__file__)
        ascii_images_dir = os.path.join(current_dir, 'ascii_images')
    
    assert speed_multiplier >= 1.0, "Speed multiplier must be greater than 1.0. Slowing down videos is not supported."
    assert num_sub_images_width > 0, "num_sub_images_width must be greater than 0"
    assert os.path.exists(input_video_path), f"Input video file does not exist: {input_video_path}"
    assert os.path.exists(ascii_images_dir), f"ASCII images directory does not exist: {ascii_images_dir}"
    assert input_video_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')), "Unsupported video format. Supported formats: .mp4, .avi, .mov, .mkv"
    assert output_video_path.lower().endswith(('.mp4', '.avi')), "Output video format must be .mp4 or .avi"
    assert start_time >= 0, "Start time must be non-negative"
    assert end_time is None or end_time > start_time, "End time must be greater than start time"
    # Open the video file
    cap = cv2.VideoCapture(input_video_path)
    
    # Check if the video was opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video file: {input_video_path}")
        return False
        
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # If end_time is None, use the entire video
    if end_time is None:
        end_time = total_frames / fps
    
    # Create temporary file paths for frame processing
    temp_frame_path = "temp_frame.png"
    temp_ascii_path = "temp_ascii.png"
    
    # Calculate start and end frame numbers
    start_frame = int(start_time * fps)
    end_frame = min(int(end_time * fps), total_frames - 1)
        
    # Set the video to start at the start_frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    # Define the codec and create VideoWriter object
    # For ASCII art, we'll use grayscale output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=False)
    
    frame_count = start_frame
    frames_written = 0
    
    # Process each frame with progress bar
    progress_bar = tqdm(total=end_frame-start_frame, desc="Converting frames", unit="frames")
    
    success = False
    try:
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
                num_sub_images_width,
                ascii_images_dir
            )

            # Write the ASCII frame to output video
            out.write(ascii_frame)
            frames_written += 1
            
            frame_count += 1
            progress_bar.update(1)
        
        progress_bar.close()
        success = True
        
    except Exception as e:
        print(f"Error during video processing: {e}")
        success = False
        
    finally:
        # Release resources
        cap.release()
        out.release()
        
        # Clean up temporary files
        if os.path.exists(temp_frame_path):
            os.remove(temp_frame_path)
        if os.path.exists(temp_ascii_path):
            os.remove(temp_ascii_path)
    
    # Compress the output video if requested (after resources are released)
    if success and compress_output and os.path.exists(output_video_path):
        try:
            # Get original file size before compression
            original_size = os.path.getsize(output_video_path)
            
            compressed_path = compress_video(
                input_path=output_video_path,
                compression_level=compression_level
            )
            
            if compressed_path and os.path.exists(compressed_path):
                # Get compressed file size
                compressed_size = os.path.getsize(compressed_path)
                
                # Calculate savings
                size_saved = original_size - compressed_size
                percentage_saved = (size_saved / original_size) * 100 if original_size > 0 else 0
                
                # Replace original with compressed version
                if os.path.exists(output_video_path):
                    os.remove(output_video_path)
                os.rename(compressed_path, output_video_path)
                
                # Print compression results
                print(f"Original size: {original_size / (1024*1024):.2f} MB → Compressed size: {compressed_size / (1024*1024):.2f} MB")
            else:
                print("Compression failed, keeping original video")
        except Exception as e:
            print(f"Compression error: {e}, keeping original video")
    
    return success

# Example usage
if __name__ == "__main__":
    # Example 1: Convert entire video with default settings
    input_video = r"example_videos\7098041-uhd_3840_2160_30fps.mp4"
    output_video = r"output\7098041-uhd_3840_2160_30fps_ascii.mp4"

    success = convert_video_to_ascii(
         input_video_path=input_video,
         output_video_path=output_video,
         start_time=0.0,          # Start at 0 seconds
         end_time=None,            # End at end of video
         num_sub_images_width=15,   
         speed_multiplier=1.0,
         ascii_images_dir="ascii_art_generator\\ascii_images")
    if success:
        print("Video conversion successful!")
    else:
        print("Video conversion failed!")