#!/usr/bin/env python

import argparse
import cv2
import time
from lane_detection.detector import LaneDetector
from lane_detection.visualizer import LaneVisualizer


def process_video(input_path, output_path, visualize=False):
    """Process a video file for lane detection.
    
    Args:
        input_path (str): Path to input video file
        output_path (str): Path to save processed video
        visualize (bool): Whether to display processing in a window
    """
    # Initialize detector and visualizer
    detector = LaneDetector()
    visualizer = LaneVisualizer()
    
    # Open video file
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError(f"Error opening video file: {input_path}")
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    processing_times = []
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Measure processing time
            start_time = time.time()
            
            # Detect lanes
            lanes = detector.detect(frame)
            
            # Visualize lanes
            result_frame = visualizer.draw_lanes(frame, lanes)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            processing_times.append(processing_time)
            
            # Write frame to output video
            writer.write(result_frame)
            
            # Display result if requested
            if visualize:
                cv2.imshow('Lane Detection', result_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            frame_count += 1
            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames")
    
    finally:
        # Release resources
        cap.release()
        writer.release()
        cv2.destroyAllWindows()
        
        # Print performance stats
        if processing_times:
            avg_time = sum(processing_times) / len(processing_times)
            print(f"Processed {frame_count} frames")
            print(f"Average processing time: {avg_time:.4f} seconds per frame")
            print(f"Average FPS: {1/avg_time:.2f}")


def main():
    parser = argparse.ArgumentParser(description='Lane Detection System')
    parser.add_argument('--input', '-i', required=True, help='Path to input video file')
    parser.add_argument('--output', '-o', required=True, help='Path to output video file')
    parser.add_argument('--visualize', '-v', action='store_true', help='Visualize processing')
    
    args = parser.parse_args()
    
    print(f"Processing video: {args.input}")
    print(f"Output will be saved to: {args.output}")
    
    process_video(args.input, args.output, args.visualize)
    
    print("Processing complete!")


if __name__ == "__main__":
    main()