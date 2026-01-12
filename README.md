# ASCII Art Generator

A Python-based ASCII art generator that converts images and videos into beautiful ASCII art representations using individual character images.

## Quick Start

**New to ASCII art generation?** Check out our [Interactive Jupyter Tutorial](ascii_art_tutorial.ipynb) for hands-on examples and step-by-step guidance!

<div align="center">
  <img src="output/village_image.png" alt="ASCII Art Example" width="400"/>
</div>

*High-resolution ASCII art generated from an original image*

## Animated Examples

GIFs are fully supported in markdown and work great on GitHub pages! Here's how to showcase animated ASCII art:

### Video to ASCII Art Demo
```markdown
![ASCII Video Demo](assets/ascii_video_demo.gif)
```

<div align="center">
  <img src="assets/ascii_video_demo.gif" alt="ASCII Video Demo" width="600"/>
  <br><em>Animated ASCII art video conversion</em>
</div>

## How It Works

The generator works by:
1. **Character Generation**: Creates image representations of ASCII characters (space to ~) using monospace fonts
2. **Brightness Analysis**: Calculates average brightness for each ASCII character image
3. **Image Segmentation**: Divides input images into small sub-regions
4. **Character Matching**: Maps each sub-region to the ASCII character with the closest brightness
5. **Art Assembly**: Combines all ASCII character images to create the final ASCII art

## Installation

### Option 1: Install as a Python Package (Recommended)

```bash
# Install in development mode
pip install -e .

# Or install directly from the repository
pip install git+https://github.com/yourusername/ascii_art_generator.git
```

### Option 2: Manual Installation

Make sure you have Python 3.7+ installed, then install dependencies:

```bash
pip install opencv-python numpy matplotlib pillow tqdm
```

### Option 3: For Jupyter Notebook Users

```bash
# Install with notebook extras
pip install -e .[notebook]
```

## Usage

### As a Python Module

```python
# Import the module
import ascii_art_generator
from ascii_art_generator import generate_ascii_art, convert_video_to_ascii

# Generate ASCII art from an image
ascii_result = generate_ascii_art(
    image_path='path/to/your/image.jpg',
    num_sub_images_width=150,
    output_path='output/ascii_art.png'
)

# Convert a video to ASCII art
success = convert_video_to_ascii(
    input_video_path='path/to/your/video.mp4',
    output_video_path='output/ascii_video.mp4',
    num_sub_images_width=100,
    end_time=10.0  # Process first 10 seconds
)
```

### Interactive Tutorial

**For detailed examples and step-by-step guidance, check out our [Interactive Jupyter Tutorial](ascii_art_tutorial.ipynb)!**

The tutorial covers:
- Setting up the module
- Image to ASCII art conversion
- Video to ASCII art conversion  
- Parameter optimization
- Best practices and tips

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ascii_art_generator.git
cd ascii_art_generator
```

2. Install the module:
```bash
pip install -e .
```

3. The project comes with pre-generated ASCII character images. The tutorial will guide you through generating them if needed.


## Project Structure

```
ascii_art_generator/
├── README.md
├── ascii_art_generator/
│   ├── ascii_art_generator_image.py    # Main image processing module
│   ├── ascii_art_generator_video.py    # Video processing module
│   ├── utils_ascii.py                  # ASCII character utilities
│   ├── utils_compute_stats.py          # Brightness analysis utilities
│   └── ascii_images/                   # Pre-generated ASCII character images
├── example_images/                     # Sample images for testing
├── example_videos/                     # Sample videos for testing
└── output/                            # Generated ASCII art output
```

## File Descriptions

- **ascii_art_generator_image.py**: Core image-to-ASCII conversion functionality
- **ascii_art_generator_video.py**: Video processing and frame-by-frame ASCII conversion
- **utils_ascii.py**: Utilities for generating and handling ASCII character images
- **utils_compute_stats.py**: Functions for analyzing brightness and coverage of ASCII characters

## Tips for Best Results

1. **Image Selection**: High-contrast images work best
2. **Resolution**: Start with `num_sub_images_width=100-200` for testing
3. **Video Processing**: Lower resolutions (50-100) process much faster for videos
4. **Character Enhancement**: Increase `kernel_size` and `iterations` for bold images
5. **Performance**: Video processing can be slow; consider shorter clips or lower resolution for testing

