# I want to analyse all images in ascii_images directory
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2

def compute_average_brightness(images_dir='ascii_images', kernel_size=3, iterations=4):
    """
    Compute the average brightness for all ASCII images in a directory.
    
    Args:
        images_dir (str): Path to the directory containing ASCII images
        
    Returns:
        dict: Dictionary with filename as key and average brightness as value
    """
    average_brightness = {}
    
    for filename in os.listdir(images_dir):
        file_path = os.path.join(images_dir, filename)
        ascii_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        
        if ascii_image is None:
            continue  # Skip non-image files
            
        # Erode the ascii image to enhance features
        ascii_image = cv2.erode(ascii_image, np.ones((kernel_size,kernel_size), np.uint8), iterations=iterations)
        avg_brightness = np.mean(ascii_image)
        average_brightness[filename] = avg_brightness
    
    return average_brightness

def compute_coverage(images_dir='ascii_images', kernel_size=3, iterations=4):
    """
    Compute the coverage of non-zero pixels in an ASCII image.
    
    Args:
        images_dir (str): Path to the directory containing ASCII images
    Returns:
        dict: Dictionary with filename as key and coverage ratio as value
    """
    coverage = {}
    for filename in os.listdir(images_dir):
        file_path = os.path.join(images_dir, filename)
        ascii_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        
        if ascii_image is None:
            continue  # Skip non-image files
            
        # Erode the ascii image to enhance features
        ascii_image = cv2.erode(ascii_image, np.ones((kernel_size,kernel_size), np.uint8), iterations=iterations)
        non_zero_count = np.count_nonzero(ascii_image)
        total_pixels = ascii_image.size
        coverage[filename] = non_zero_count / total_pixels
    return coverage

if __name__ == "__main__":
    # Use the function to compute brightness for all images
    average_brightness = compute_average_brightness('ascii_images', kernel_size=3, iterations=4)
    coverage = compute_coverage('ascii_images', kernel_size=3, iterations=4)

    plt.hist([brightness for _, brightness in average_brightness.items()], bins=26, color='blue', alpha=0.7)
    plt.title('Histogram of Average Brightness of ASCII Images')
    plt.show()

    plt.hist([cov for _, cov in coverage.items()], bins=26, color='green', alpha=0.7)
    plt.title('Histogram of Coverage of ASCII Images')
    plt.show()