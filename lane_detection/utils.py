"""Utility functions for lane detection."""

import cv2
import numpy as np


def grayscale(img):
    """Convert image to grayscale.
    
    Args:
        img: Input image (BGR color space)
        
    Returns:
        Grayscale image
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def gaussian_blur(img, kernel_size=5):
    """Apply Gaussian blur to reduce noise.
    
    Args:
        img: Input image
        kernel_size: Size of Gaussian kernel
        
    Returns:
        Blurred image
    """
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def canny(img, low_threshold=50, high_threshold=150):
    """Apply Canny edge detection algorithm.
    
    Args:
        img: Input image (grayscale)
        low_threshold: Lower threshold for edge detection
        high_threshold: Upper threshold for edge detection
        
    Returns:
        Image with detected edges
    """
    return cv2.Canny(img, low_threshold, high_threshold)


def region_of_interest(img, vertices):
    """Mask the image to only include the region of interest.
    
    Args:
        img: Input image
        vertices: Array of vertices defining the region of interest
        
    Returns:
        Masked image showing only the region of interest
    """
    # Create an empty mask with the same shape as the input image
    mask = np.zeros_like(img)
    
    # Define the number of channels in the mask
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # Color image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255  # Grayscale image
    
    # Fill the region of interest with white color
    cv2.fillPoly(mask, [vertices], ignore_mask_color)
    
    # Apply the mask to the input image
    masked_image = cv2.bitwise_and(img, mask)
    
    return masked_image


def get_hough_lines(img, rho=1, theta=np.pi/180, threshold=15, min_line_len=40, max_line_gap=20):
    """Detect lines in the image using Hough transform.
    
    Args:
        img: Input edge image
        rho: Distance resolution in pixels
        theta: Angle resolution in radians
        threshold: Minimum number of votes
        min_line_len: Minimum line length
        max_line_gap: Maximum allowed gap between line segments
        
    Returns:
        Array of detected line segments
    """
    return cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), 
                          minLineLength=min_line_len, maxLineGap=max_line_gap)


def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """Blend two images.
    
    Args:
        img: First image (colored lanes)
        initial_img: Second image (original frame)
        α: Weight of the first image
        β: Weight of the second image
        γ: Scalar added to each sum
        
    Returns:
        Blended image: img * α + initial_img * β + γ
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)


def calculate_lane_lines(lines, image_height):
    """Calculate left and right lane lines from a set of line segments.
    
    Args:
        lines: Array of detected line segments
        image_height: Height of the original image
        
    Returns:
        Tuple (left_line, right_line) representing the extrapolated lane lines
    """
    if lines is None:
        return None, None
    
    left_lines = []  # (slope, intercept)
    right_lines = []  # (slope, intercept)
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2:  # Skip vertical lines
                continue
            
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
            
            # Categorize lines by slope
            if slope < -0.3:  # Left line
                left_lines.append((slope, intercept))
            elif slope > 0.3:  # Right line
                right_lines.append((slope, intercept))
    
    # Average out the lines
    left_line = None
    right_line = None
    
    if left_lines:
        left_avg = np.average(left_lines, axis=0)
        slope, intercept = left_avg
        y1 = image_height  # Bottom of the image
        y2 = int(y1 * 0.6)  # A point higher up (60% from bottom)
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        left_line = ((x1, y1), (x2, y2))
    
    if right_lines:
        right_avg = np.average(right_lines, axis=0)
        slope, intercept = right_avg
        y1 = image_height  # Bottom of the image
        y2 = int(y1 * 0.6)  # A point higher up (60% from bottom)
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        right_line = ((x1, y1), (x2, y2))
    
    return left_line, right_line