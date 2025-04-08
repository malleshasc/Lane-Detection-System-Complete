# Lane Detection System

A complete Python-based lane detection system for processing road videos on Windows machines.

## Overview

This project implements a computer vision-based lane detection system that can:
- Process video frames to identify lane markings on roads
- Highlight detected lanes with visual overlays
- Output processed video with lane markings highlighted
- Detect lane departures (optional feature)

## Project Structure

```
./
├── data/               # Sample videos and test data
│   ├── sample_video.mp4
│   └── test_frames/    # Test frames for unit testing
├── lane_detection/     # Core lane detection module
│   ├── __init__.py
│   ├── detector.py     # Lane detection implementation
│   ├── utils.py        # Utility functions
│   └── visualizer.py   # Visualization tools for detected lanes
├── tests/              # Test suite
│   ├── __init__.py
│   ├── test_detector.py
│   ├── test_utils.py
│   └── test_visualizer.py
├── scripts/            # Helper scripts
│   └── pipeline.py     # CI/CD pipeline script
├── requirements.txt    # Project dependencies
├── setup.py            # Package setup configuration
└── main.py             # Entry point for running the application
```

## Installation

```bash
# Clone the repository
git clone https://github.com/username/Lane-Detection-System.git
cd Lane-Detection-System

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Usage

```bash
# Process a video file
python main.py --input data/sample_video.mp4 --output output_video.mp4

# Run with visualization (displays output in a window)
python main.py --input data/sample_video.mp4 --output output_video.mp4 --visualize
```

## Testing

```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=lane_detection tests/

# Generate coverage report
python -m pytest --cov=lane_detection --cov-report=html tests/
```

## CI/CD Pipeline

The project includes a pipeline script that:
- Runs all tests
- Checks for 100% test coverage
- Automatically merges code into the `prod` branch if all tests pass

To run the pipeline:

```bash
python scripts/pipeline.py
```

## License

MIT

## Credits

Sample video from Udacity Self-Driving Car Dataset (if applicable)