from .ascii_art_generator_image import generate_ascii_art
from .ascii_art_generator_video import convert_video_to_ascii
from .utils_ascii import generate_ascii_images, get_ascii_char, get_ascii_code
from .utils_compute_stats import compute_average_brightness

__version__ = "1.0.0"
__author__ = "Jannik Wege"

__all__ = [
    'generate_ascii_art',
    'convert_video_to_ascii', 
    'generate_ascii_images',
    'get_ascii_char',
    'get_ascii_code',
    'compute_average_brightness'
]