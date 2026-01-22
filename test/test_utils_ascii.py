import pytest
import sys
import os

# I want to write test for my function in the module utils_ascii.py in the module ascii_art_generator
from ascii_art_generator.utils_ascii import generate_ascii_images, get_ascii_char, get_ascii_code,monospace_char_image

def test_get_ascii_char():
    assert get_ascii_char(65) == 'A'
    assert get_ascii_char(97) == 'a'
    assert get_ascii_char(48) == '0'
    assert get_ascii_char(32) == ' '
    assert get_ascii_char(126) == '~'
    # Test invalid input - function returns error string instead of raising exception
    result = get_ascii_char(200)
    assert result.startswith("Error:")
    
def test_get_ascii_code():
    assert get_ascii_code('A') == 65
    assert get_ascii_code('a') == 97
    assert get_ascii_code('0') == 48
    assert get_ascii_code(' ') == 32
    assert get_ascii_code('~') == 126
    # Test invalid input - function returns error string instead of raising exception
    result = get_ascii_code('€')
    assert result.startswith("Error:")

def test_inverse_property():
    for code in range(32, 127):
        char = get_ascii_char(code)
        assert get_ascii_code(char) == code
