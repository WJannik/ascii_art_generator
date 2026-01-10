import numpy as np
from PIL import Image, ImageDraw, ImageFont

def get_ascii_char(number):
    """
    Convert an integer (0-127) to its ASCII character.
    
    Args:
        number: Integer from 0 to 127
    
    Returns:
        The corresponding ASCII character as a string
    """
    if not isinstance(number, int) or number < 0 or number > 127:
        return f"Error: Number must be between 0 and 127, got {number}"
    
    return chr(number)

def get_ascii_code(character):
    """
    Convert a single ASCII character to its integer code (0-127).
    
    Args:
        character: A single ASCII character string
    
    Returns:
        The corresponding ASCII integer code
    """
    if not isinstance(character, str) or len(character) != 1:
        return f"Error: Input must be a single character string, got {character}"
    
    code = ord(character)
    if code < 0 or code > 127:
        return f"Error: Character must be an ASCII character (0-127), got {character}"
    
    return code


def monospace_char_image(char, font_name = None, font_size=32, out_path="char.png", fixed_size=None):
    """
    Create an image of a single ASCII character using a monospace font.
    All images will have the same dimensions for consistency.
    
    Args:
        char: Single character to render
        font_size: Size of the font (default 120)
        out_path: Output file path (default "char.png")
        fixed_size: Tuple (width, height) for consistent image size
    
    Returns:
        PIL Image object
    """
    try:
        # Try to load a monospaced font - fallback to default if not found
        monospace_fonts = [
            # Windows common monospace fonts
            "cour.ttf",           # Courier New (Windows)
            "Courier New.ttf",    # Courier New (full name)
            "consola.ttf",        # Consolas (Windows)
            "Consolas.ttf",       # Consolas (full name)
            "lucon.ttf",          # Lucida Console
            "Lucida Console.ttf", # Lucida Console (full name)
            
            # Cross-platform monospace fonts
            "DejaVuSansMono.ttf",      # DejaVu Sans Mono
            "DejaVu Sans Mono.ttf",    # DejaVu Sans Mono (spaces)
            "LiberationMono-Regular.ttf", # Liberation Mono
            "FiraCode-Regular.ttf",    # Fira Code (programming font)
            "JetBrainsMono-Regular.ttf", # JetBrains Mono
            "SourceCodePro-Regular.ttf", # Source Code Pro
            
            # macOS/Linux common fonts
            "Monaco.ttf",         # Monaco (macOS)
            "Menlo.ttf",         # Menlo (macOS)
            "courier.ttf",       # Generic courier
            
            # Fallback system fonts
            "C:/Windows/Fonts/cour.ttf",     # Windows system path
            "C:/Windows/Fonts/consola.ttf",  # Windows Consolas
        ]

        font = None
        # Pick random font from the list if font_name is not provided
        if font_name is None:
            font_name = np.random.choice(monospace_fonts)
        try:
            font = ImageFont.truetype(font_name, size=font_size)
            print(f"Using font: {font_name}")
        except (OSError, IOError):
            print(f"Could not load font '{font_name}'. Trying default monospace font.")
            pass
        
        # If no TrueType font found, use default
        if font is None:
            print("Using default font (no TrueType monospace font found)")
            font = ImageFont.load_default()
        # Calculate consistent dimensions for all characters
        if fixed_size is None:
            # Use a wide character to determine maximum dimensions
            dummy = Image.new("RGB", (1, 1))
            draw = ImageDraw.Draw(dummy)
            
            # Test with 'W' which is typically the widest character in monospace fonts
            test_bbox = draw.textbbox((0, 0), 'W', font=font)
            max_w = test_bbox[2] - test_bbox[0]
            max_h = test_bbox[3] - test_bbox[1]
            
            # Add padding for consistent appearance
            padding = 0
            fixed_size = (max_w + padding, max_h + padding)

        # Create image with fixed dimensions
        img = Image.new("RGB", fixed_size, "white")
        draw = ImageDraw.Draw(img)
        
        # Calculate center position for the text
        center_x = fixed_size[0] // 2
        center_y = fixed_size[1] // 2
        
        # Get the bounding box to find the actual text dimensions
        bbox = draw.textbbox((0, 0), char, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        # Offset by half the text dimensions and account for the bbox offset
        x = center_x - text_width // 2 - bbox[0]
        y = center_y - text_height // 2 - bbox[1]
        
        # Draw the character centered in the image
        draw.text((x, y), char, fill="black", font=font)

        img.save(out_path)
        return img
    
    
    except Exception as e:
        print(f"Error creating image for character '{char}': {e}")
        return None


def generate_ascii_images(start_code=32, end_code=126, output_dir="ascii_images", font_name = None, font_size=32):
    """
    Generate images for a range of ASCII characters.
    All images will have consistent dimensions.
    
    Args:
        start_code: Starting ASCII code (default 32, space)
        end_code: Ending ASCII code (default 126, ~)
        output_dir: Directory to save images (default "ascii_images")
        font_size: Font size to use for all characters
    """
    import os
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate fixed size once for all characters
    try:
        # Load the same font that will be used for characters (use same list as main function)
        monospace_fonts = [
            "cour.ttf", "Courier New.ttf", "consola.ttf", "Consolas.ttf", 
            "lucon.ttf", "Lucida Console.ttf", "DejaVuSansMono.ttf", 
            "DejaVu Sans Mono.ttf", "LiberationMono-Regular.ttf",
            "FiraCode-Regular.ttf", "JetBrainsMono-Regular.ttf",
            "SourceCodePro-Regular.ttf", "Monaco.ttf", "Menlo.ttf", "courier.ttf",
            "C:/Windows/Fonts/cour.ttf", "C:/Windows/Fonts/consola.ttf"
        ]
        
        font = None
        # Pick random font from the list if font_name is not provided
        if font_name is None:
            font_name = np.random.choice(monospace_fonts)
        try:
            font = ImageFont.truetype(font_name, size=font_size)
            print(f"Using font: {font_name}")
        except (OSError, IOError):
            print(f"Could not load font '{font_name}'. Trying default monospace font.")
            pass
        if font is None:
            font = ImageFont.load_default()
        
        # Calculate consistent dimensions using the widest character
        dummy = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(dummy)
        test_bbox = draw.textbbox((0, 0), 'W', font=font)
        max_w = test_bbox[2] - test_bbox[0]
        max_h = test_bbox[3] - test_bbox[1]
        padding = 0
        fixed_size = (max_w + padding, max_h + padding)
        
        print(f"Using fixed image size: {fixed_size[0]}x{fixed_size[1]} pixels")
        
    except Exception as e:
        print(f"Error calculating fixed size: {e}")
        fixed_size = (32, 32)  # Fallback size
    
    # Generate images with consistent size
    for code in range(start_code, end_code + 1):
        char = chr(code)
        # Handle special characters in filenames
        if char == ' ':
            filename = f"ascii_{code:03d}_space.png"
        elif char in '<>:"/\\|?*':
            filename = f"ascii_{code:03d}.png"
        else:
            filename = f"ascii_{code:03d}_{char}.png"
            
        filepath = os.path.join(output_dir, filename)
        print(f"Generating image for ASCII {code} ('{char}') -> {filename}")
        monospace_char_image(char, font_name=font_name, font_size=font_size, out_path=filepath, fixed_size=fixed_size)


if __name__ == "__main__":
    # Example: render ASCII code 65 ('A')
    monospace_char_image(chr(65))
    
    # Generate images for printable ASCII characters
    generate_ascii_images()
