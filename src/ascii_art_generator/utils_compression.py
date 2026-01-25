import cv2
import os
from tqdm import tqdm


def compress_video(input_path, output_path=None, compression_level='medium'):
    """
    Compress a video file to reduce file size using OpenCV.
    
    Args:
        input_path (str): Path to the input video file
        output_path (str): Path for compressed output (default: adds '_compressed' suffix)
        compression_level (str): Compression level - 'low', 'medium', 'high' (default: 'medium')
        
    Returns:
        str: Path to the compressed video file, or None if compression failed
    """
    if output_path is None:
        name, ext = os.path.splitext(input_path)
        output_path = f"{name}_compressed{ext}"
    
    # OpenCV compression
    try:        
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error: Could not open video for compression: {input_path}")
            return None
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Compression settings based on level
        if compression_level == 'low':
            quality = 0.3  # Lower quality
        elif compression_level == 'medium':
            quality = 0.5  # Medium quality
        elif compression_level == 'high':
            quality = 0.7  # Higher quality
        else:
            quality = 0.5
        
        # Create compressed video writer with higher compression
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)
        
        frame_count = 0
        progress_bar = tqdm(total=total_frames, desc="Compressing frames", unit="frames")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Apply quality reduction by resizing and back (lossy compression)
            if quality < 1.0:
                h, w = frame.shape[:2]
                new_h, new_w = int(h * quality), int(w * quality)
                compressed_frame = cv2.resize(frame, (new_w, new_h))
                frame = cv2.resize(compressed_frame, (w, h))
            
            out.write(frame)
            frame_count += 1
            progress_bar.update(1)
        
        progress_bar.close()
        cap.release()
        out.release()
        return output_path
        
    except Exception as e:
        print(f"OpenCV compression error: {e}")
        return None