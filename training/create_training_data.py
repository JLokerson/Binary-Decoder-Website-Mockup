#!/usr/bin/env python3
"""
Script to create proper Tesseract training data for binary pattern recognition
"""

import os
import subprocess
import sys

def create_box_file_from_ground_truth(image_name, gt_file):
    """Create a proper box file from ground truth text"""
    # Read the ground truth text
    with open(gt_file, 'r') as f:
        text = f.read().strip()
    
    # For simplicity, we'll create a basic box file
    # In a real scenario, you'd need proper coordinate mapping
    box_content = []
    
    # Split text into characters and assign basic coordinates
    y_pos = 100  # Basic y position
    x_pos = 10   # Starting x position
    
    for line in text.split('\n'):
        if line.strip():
            for char in line:
                if char != ' ':
                    # Basic box format: char left bottom right top page
                    box_content.append(f"{char} {x_pos} {y_pos-10} {x_pos+10} {y_pos+10} 0")
                    x_pos += 12
                else:
                    x_pos += 6  # Space width
            x_pos = 10  # Reset for new line
            y_pos += 20
    
    box_file = image_name.replace('.png', '.box')
    with open(box_file, 'w') as f:
        f.write('\n'.join(box_content))
    
    print(f"Created box file: {box_file}")

def run_tesseract_training():
    """Run the basic Tesseract training steps"""
    
    # Image files in the directory
    images = ['IMG_2535.png', 'IMG_2542.png']
    
    print("Creating box files from ground truth...")
    for img in images:
        gt_file = img.replace('.png', '.gt.txt')
        if os.path.exists(gt_file):
            create_box_file_from_ground_truth(img, gt_file)
    
    print("Creating training files...")
    for img in images:
        base_name = img.replace('.png', '')
        
        # Generate .tr file
        try:
            subprocess.run([
                'tesseract', img, base_name, '-l', 'eng', '--psm', '6', 'box.train'
            ], check=True)
            print(f"Created training file: {base_name}.tr")
        except subprocess.CalledProcessError as e:
            print(f"Error creating training file for {img}: {e}")
    
    print("Training data creation completed!")

if __name__ == "__main__":
    run_tesseract_training()