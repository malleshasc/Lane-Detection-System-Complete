from setuptools import setup, find_packages

setup(
    name="lane_detection",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "opencv-python>=4.5.0",
        "matplotlib>=3.3.0",
        "scipy>=1.7.0",
        "pillow>=8.2.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Lane detection system for road videos",
    keywords="computer vision, lane detection, autonomous driving",
    python_requires='>=3.7',
)