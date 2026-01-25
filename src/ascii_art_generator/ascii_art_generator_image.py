import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

from .utils_ascii import generate_ascii_images
from .utils_compute_stats import compute_average_brightness


def generate_ascii_art(image_path, ascii_images_dir='ascii_images', num_sub_images_width=200, kernel_size=3, iterations=4,
                       output_path='generated_ascii_art_image.png',plot_enabled =True, save_enabled=True, generate_ascii_images_flag=False):
    """
    Generate ASCII art from a given image path.
    
    Args:
        image_path (str): Path to the input image
        ascii_images_dir (str): Directory containing ASCII character images
        num_sub_images_width (int): Number of sub-images in width dimension (controls resolution)
        output_path (str): Path to save the generated ASCII art image
        
    Returns:
        numpy.ndarray: The generated ASCII art image
    """
    # Generate images for printable ASCII characters, if needed
    if generate_ascii_images_flag:
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
    
    # Read in ASCII image and get their dimensions
    ascii_aspect_ratio = get_aspect_ratio_of_ascii_image()

    # Calculate sub-image dimensions
    size_sub_image_width = width // num_sub_images_width
    size_sub_image_height = int(size_sub_image_width / ascii_aspect_ratio)
    num_sub_images_height = int(np.ceil(height / size_sub_image_height))
    num_sub_images_width_actual = int(np.ceil(width / size_sub_image_width)) # This might be 1 more than the original num_sub_images_width due to ceiling
    
    # Preload and pre-scale all ASCII images for better performance
    ascii_images_cache = preload_ascii_images(ascii_images_dir, size_sub_image_width, size_sub_image_height, average_brightness)
    
    # Create empty ASCII art image with same dimensions as input image
    ascii_art_image = np.zeros((height, width), dtype=np.uint8)

    # Process each sub-image
    for i in (range(num_sub_images_height)):
        for j in range(num_sub_images_width_actual): 
            # Calculate boundaries of the sub-image
            start_y = i * size_sub_image_height
            end_y = min((i + 1) * size_sub_image_height, height)
            start_x = j * size_sub_image_width
            end_x = min((j + 1) * size_sub_image_width, width)
            
            # Extract sub-image
            sub_image = gray_image[start_y:end_y, start_x:end_x]
            avg_brightness = np.mean(sub_image)
            
            # Find the ASCII character that best matches the brightness
            closest_match = min(sorted_brightness, key=lambda x: abs(x[1] - avg_brightness))
            
            # Get the pre-loaded and pre-scaled ASCII image
            ascii_image_resized = ascii_images_cache[closest_match[0]]
            
            # For partial areas/edges, crop the resized image to fit
            actual_height = end_y - start_y
            actual_width = end_x - start_x
            ascii_image_cropped = ascii_image_resized[:actual_height, :actual_width]
            
            # Place the ASCII image into the final image
            ascii_art_image[start_y:end_y, start_x:end_x] = ascii_image_cropped
    
    # Save the generated ASCII art image
    if save_enabled:
        cv2.imwrite(output_path, ascii_art_image)

    # Plotting the original and ASCII art image
    if plot_enabled:
        # Display the result
        plt.subplot(1, 2, 1)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), cmap=None)
        plt.title('Original Image')
        plt.axis('off')
        
        plt.subplot(1, 2, 2)
        plt.imshow(ascii_art_image, cmap='gray')
        plt.title('Generated ASCII Art')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    return ascii_art_image


def get_aspect_ratio_of_ascii_image():
    """ Compute the aspect ratio of ASCII character images by dividing width by height. """
    # Read in ASCII image and get their dimensions
    import os
    current_dir = os.path.dirname(__file__)
    path_to_ascii = os.path.join(current_dir, 'ascii_images')
    ascii_image_sample = cv2.imread(os.path.join(path_to_ascii, os.listdir(path_to_ascii)[1]), cv2.IMREAD_GRAYSCALE)
    ascii_image_height, ascii_image_width = ascii_image_sample.shape
    ascii_aspect_ratio = ascii_image_width / ascii_image_height
    return ascii_aspect_ratio

def preload_ascii_images(ascii_images_dir, size_sub_image_width, size_sub_image_height, average_brightness):
    """ Preload and pre-scale all ASCII images for better performance.
    Args:
        ascii_images_dir (str): Directory containing ASCII character images
        size_sub_image_width (int): Width to resize ASCII images to
        size_sub_image_height (int): Height to resize ASCII images to
        average_brightness (dict): Dictionary of average brightness for each ASCII character image
    Returns:
        dict: Dictionary mapping filenames to pre-scaled ASCII images
    """
    # Preload and pre-scale all ASCII images for better performance
    ascii_images_cache = {}
    for filename, brightness in average_brightness.items():
        ascii_image_path = os.path.join(ascii_images_dir, filename)
        ascii_image = cv2.imread(ascii_image_path, cv2.IMREAD_GRAYSCALE)
        # Pre-resize to standard size
        ascii_image_resized = cv2.resize(ascii_image, (size_sub_image_width, size_sub_image_height))
        ascii_images_cache[filename] = ascii_image_resized
    return ascii_images_cache

if __name__ == "__main__":
    # Apply ASCII art generation for some sample images stored in './example_images' directory
    for image_path in os.listdir('./example_images'):
        if image_path.endswith('.jpg') or image_path.endswith('.png'):
            print(f'Generating ASCII art for image: {image_path}')
            ascii_art = generate_ascii_art(
                image_path=os.path.join('./example_images', image_path),
                ascii_images_dir='ascii_art_generator\\ascii_images',
                num_sub_images_width=150,
                output_path=f'./output/generated_ascii_art_{os.path.splitext(image_path)[0]}.png',
                plot_enabled=False,
                save_enabled=True
            )