# I want to analyse all images in ascii_images directory
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2

def compute_average_brightness(images_dir='ascii_images'):
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
        ascii_image = cv2.erode(ascii_image, np.ones((3,3), np.uint8), iterations=1)
        avg_brightness = np.mean(ascii_image)
        average_brightness[filename] = avg_brightness
    
    return average_brightness

if __name__ == "__main__":
    # Use the function to compute brightness for all images
    average_brightness = compute_average_brightness('ascii_images')

    # Also compute coverage (keeping existing functionality)
    coverage = {}
    acii_images_dir = 'ascii_images'
    for filename in os.listdir(acii_images_dir)[:]:
        ascii_image = cv2.imread(os.path.join(acii_images_dir, filename), cv2.IMREAD_GRAYSCALE)
        if ascii_image is None:
            continue
        ascii_image = cv2.erode(ascii_image, np.ones((3,3), np.uint8), iterations=1)
        coverage[filename] = np.count_nonzero(ascii_image) / ascii_image.size

    plt.hist([brightness for _, brightness in average_brightness.items()], bins=10, color='blue', alpha=0.7)
    plt.title('Histogram of Average Brightness of ASCII Images')
    plt.show()

    plt.hist([cov for _, cov in coverage.items()], bins=10, color='green', alpha=0.7)
    plt.title('Histogram of Coverage of ASCII Images')
    plt.show()