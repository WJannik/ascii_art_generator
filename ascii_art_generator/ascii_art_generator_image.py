import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from ascii_art_generator.utils_ascii import generate_ascii_images
from utils_compute_stats import compute_average_brightness

def generate_ascii_art(image_path, ascii_images_dir='ascii_images', num_sub_images_x=200, kernel_size=3, iterations=4,
                       output_path='generated_ascii_art_image.png',plot_enabled =True, save_enabled=True):
    """
    Generate ASCII art from a given image path.
    
    Args:
        image_path (str): Path to the input image
        ascii_images_dir (str): Directory containing ASCII character images
        num_sub_images_x (int): Number of sub-images in x dimension (controls resolution)
        output_path (str): Path to save the generated ASCII art image
        
    Returns:
        numpy.ndarray: The generated ASCII art image
    """
    # Generate images for printable ASCII characters
    generate_ascii_images()

    # Get brightness values for ASCII characters
    average_brightness = compute_average_brightness(ascii_images_dir, kernel_size, iterations)
    sorted_brightness = sorted(average_brightness.items(), key=lambda x: x[1])

    # Read and process input image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image from path: {image_path}")
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray_image.shape
    print(f'Input image dimensions: {width}x{height}')
    
    # Read in ASCII image and get their dimensions
    ascii_aspect_ratio = get_aspect_ratio_of_ascii_image()

    # Calculate sub-image dimensions
    size_sub_image_x = width // num_sub_images_x
    size_sub_image_y = int(size_sub_image_x / ascii_aspect_ratio)
    num_sub_images_y = int(np.ceil(height / size_sub_image_y))  # Use ceil to include partial sub-images
    # Also need to handle partial sub-images on the right edge
    num_sub_images_x_actual = int(np.ceil(width / size_sub_image_x))  # Actual number including partial ones
    
    
    # Preload and pre-scale all ASCII images for better performance
    ascii_images_cache = preload_ascii_images(ascii_images_dir, size_sub_image_x, size_sub_image_y, average_brightness)
    
    # Create empty ASCII art image with same dimensions as input
    ascii_art_image = np.zeros((height, width), dtype=np.uint8)
    
    # Process each sub-image, including partial ones on edges
    for i in (range(num_sub_images_y)):
        for j in range(num_sub_images_x_actual):  # Use actual number including partial ones
            # Calculate boundaries, ensuring we don't exceed image dimensions
            start_y = i * size_sub_image_y
            end_y = min((i + 1) * size_sub_image_y, height)
            start_x = j * size_sub_image_x
            end_x = min((j + 1) * size_sub_image_x, width)
            
            # Extract sub-image (may be partial on edges)
            sub_image = gray_image[start_y:end_y, start_x:end_x]
            avg_brightness = np.mean(sub_image)
            
            # Find the ASCII character that best matches the brightness
            closest_match = min(sorted_brightness, key=lambda x: abs(x[1] - avg_brightness))
            
            # Get the pre-loaded and pre-scaled ASCII image
            ascii_image_resized = ascii_images_cache[closest_match[0]]
            
            # For partial areas (edges), crop the resized image to fit
            actual_height = end_y - start_y
            actual_width = end_x - start_x
            ascii_image_cropped = ascii_image_resized[:actual_height, :actual_width]
            
            # Place the (possibly cropped) ASCII image into the final image
            ascii_art_image[start_y:end_y, start_x:end_x] = ascii_image_cropped
    
    if save_enabled:
        # Save the generated ASCII art
        cv2.imwrite(output_path, ascii_art_image)
        print(f'ASCII art saved to: {output_path}')

    if plot_enabled:
        # Display the result
        plt.figure(figsize=(12, 8))
        plt.subplot(1, 2, 1)
        plt.imshow(gray_image, cmap='gray')
        plt.axis('off')
        
        plt.subplot(1, 2, 2)
        plt.imshow(ascii_art_image, cmap='gray')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    return ascii_art_image


def get_aspect_ratio_of_ascii_image():
    # Read in ASCII image and get their dimensions
    path_to_ascii = 'ascii_images'
    print(os.listdir(path_to_ascii)[0])
    ascii_image_sample = cv2.imread(os.path.join(path_to_ascii, os.listdir(path_to_ascii)[1]), cv2.IMREAD_GRAYSCALE)
    ascii_image_height, ascii_image_width = ascii_image_sample.shape
    ascii_aspect_ratio = ascii_image_width / ascii_image_height
    return ascii_aspect_ratio

def preload_ascii_images(ascii_images_dir, size_sub_image_x, size_sub_image_y, average_brightness):
    # Preload and pre-scale all ASCII images for better performance
    ascii_images_cache = {}
    for filename, brightness in average_brightness.items():
        ascii_image_path = os.path.join(ascii_images_dir, filename)
        ascii_image = cv2.imread(ascii_image_path, cv2.IMREAD_GRAYSCALE)
        # Pre-resize to standard size
        ascii_image_resized = cv2.resize(ascii_image, (size_sub_image_x, size_sub_image_y))
        ascii_images_cache[filename] = ascii_image_resized
    return ascii_images_cache

# Example usage - you can uncomment and modify the path as needed
# image_path = r'path_to_your_image.jpg'
# ascii_art = generate_ascii_art(image_path)
if __name__ == "__main__":
    # Example usage - replace with your desired image path
    image_path = r'test_image.jpg'
    
    # Generate ASCII art with default settings
    ascii_art = generate_ascii_art(
        image_path=image_path,
        ascii_images_dir='ascii_images',
        num_sub_images_x=200,
        output_path='generated_ascii_art_image.png'
    )