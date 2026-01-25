from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ascii-art-generator",
    version="1.0.0",
    author="Jannik Wege",
    author_email="jannik.wege.1@gmx.de",
    description="A Python module for generating ASCII art from images and videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WJannik/ascii_art_generator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
        "Pillow>=8.0.0",
        "tqdm>=4.60.0",
        "ipykernel>=5.3.0",
        "ffmpeg-python>=0.2.0",
    ],
    include_package_data=True,
    package_data={
        "ascii_art_generator": ["ascii_images/*.png"],
    },
)