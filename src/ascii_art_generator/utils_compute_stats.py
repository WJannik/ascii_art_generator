import os
import matplotlib.pyplot as plt
import numpy as np
import cv2

def compute_average_brightness(images_dir='ascii_images', kernel_size=3, iterations=4):
    """
    Compute the average brightness for all ASCII images in a directory. 
    This is currently used as metric to match the subimages to ASCII characters.
    Args:
        images_dir (str): Path to the directory containing ASCII images 
        kernel_size (int): Size of the kernel for erosion
        iterations (int): Number of iterations for erosion
    Returns:
        dict: Dictionary with filename as key and average brightness as value
    """
    average_brightness = {}
    filenames = os.listdir(images_dir)
    filenames = [f for f in filenames if f.endswith('.png') or f.endswith('.jpg')]
    for filename in filenames:
        file_path = os.path.join(images_dir, filename)
        ascii_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)        
        # Erode the ascii image to enhance features
        ascii_image = cv2.erode(ascii_image, np.ones((kernel_size,kernel_size), np.uint8), iterations=iterations)
        avg_brightness = np.mean(ascii_image)
        average_brightness[filename] = avg_brightness
    
    return average_brightness

def compute_coverage(images_dir='ascii_images', kernel_size=3, iterations=4):
    """
    Compute the coverage of non-zero pixels in an ASCII image. 
    Alternative idea to average brightness for matching subimages to ASCII characters.
    Args:
        images_dir (str): Path to the directory containing ASCII images
        kernel_size (int): Size of the kernel for erosion
        iterations (int): Number of iterations for erosion
    Returns:
        dict: Dictionary with filename as key and coverage ratio as value
    """
    coverage = {}
    filenames = os.listdir(images_dir)
    filenames = [f for f in filenames if f.endswith('.png') or f.endswith('.jpg')]
    for filename in filenames:
        file_path = os.path.join(images_dir, filename)
        ascii_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)     
        # Erode the ascii image to enhance features
        ascii_image = cv2.erode(ascii_image, np.ones((kernel_size,kernel_size), np.uint8), iterations=iterations)
        non_zero_count = np.count_nonzero(ascii_image)
        total_pixels = ascii_image.size
        coverage[filename] = non_zero_count / total_pixels
    return coverage

if __name__ == "__main__":
    # Use the function to compute brightness and coverage for all ascii images
    # The goal should be to have an distribution that covers the full range from dark to bright images. 
    # More or less uniform distribution is desired.

    average_brightness = compute_average_brightness('ascii_images', kernel_size=3, iterations=4)
    coverage = compute_coverage('ascii_images', kernel_size=3, iterations=4)

    plt.hist([brightness for _, brightness in average_brightness.items()], bins=25, color='blue', alpha=0.7)
    plt.title('Histogram of Average Brightness of ASCII Images')
    plt.show()

    plt.hist([cov for _, cov in coverage.items()], bins=25, color='green', alpha=0.7)
    plt.title('Histogram of Coverage of ASCII Images')
    plt.show()