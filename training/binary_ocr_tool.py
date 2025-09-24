#!/usr/bin/env python3
"""
Binary Pattern OCR Tool for Tesseract
This script preprocesses images and applies OCR with optimized settings for binary patterns.
"""

import cv2
import numpy as np
import subprocess
import sys
import os
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_binary_image(image_path, output_path):
    """
    Preprocess image for better binary pattern recognition
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not read image: {image_path}")
        return False
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get pure binary image
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Apply morphological operations to clean up
    kernel = np.ones((2,2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # Scale up the image for better OCR
    scale_factor = 3
    height, width = binary.shape
    binary = cv2.resize(binary, (width * scale_factor, height * scale_factor), interpolation=cv2.INTER_CUBIC)
    
    # Save preprocessed image
    cv2.imwrite(output_path, binary)
    print(f"Preprocessed image saved to: {output_path}")
    return True

def run_ocr_with_custom_config(image_path, output_base):
    """
    Run OCR with optimized settings for binary patterns
    """
    # Create custom config
    custom_config = r'''
    tessedit_char_whitelist 01 
    preserve_interword_spaces 1
    '''
    
    # Save config to file
    config_file = "binary_ocr.config"
    with open(config_file, 'w') as f:
        f.write(custom_config)
    
    # Run Tesseract with custom config
    cmd = [
        'tesseract', 
        image_path, 
        output_base,
        '--psm', '6',  # Uniform block of text
        '--oem', '3',  # Default OCR Engine Mode
        '-c', 'tessedit_char_whitelist=01 ',
        '-c', 'preserve_interword_spaces=1'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"OCR completed successfully for {image_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"OCR failed for {image_path}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def process_binary_images():
    """
    Process all binary images in the current directory
    """
    images = ['IMG_2535.png', 'IMG_2542.png']
    
    for img_file in images:
        if os.path.exists(img_file):
            print(f"\nProcessing {img_file}...")
            
            # Preprocess image
            preprocessed_file = f"preprocessed_{img_file}"
            if preprocess_binary_image(img_file, preprocessed_file):
                
                # Run OCR
                output_base = img_file.replace('.png', '_ocr_result')
                if run_ocr_with_custom_config(preprocessed_file, output_base):
                    
                    # Read and display results
                    result_file = f"{output_base}.txt"
                    if os.path.exists(result_file):
                        with open(result_file, 'r') as f:
                            content = f.read().strip()
                        print(f"OCR Result for {img_file}:")
                        print(content)
                        print("-" * 50)
                    
                    # Compare with ground truth if available
                    gt_file = img_file.replace('.png', '.gt.txt')
                    if os.path.exists(gt_file):
                        with open(gt_file, 'r') as f:
                            ground_truth = f.read().strip()
                        print(f"Ground Truth for {img_file}:")
                        print(ground_truth)
                        print("-" * 50)
        else:
            print(f"Image file not found: {img_file}")

def create_custom_binary_model():
    """
    Create a simple custom model configuration for binary recognition
    """
    print("Creating custom binary recognition configuration...")
    
    # Create a simple unicharset for binary digits
    unicharset_content = """3
NULL 0 Common 0
0 8 0,255,0,255,0,0,0,0,0,0 Common 1 2 1 0
1 8 0,255,0,255,0,0,0,0,0,0 Common 2 2 2 1
"""
    
    with open('binary_custom.unicharset', 'w') as f:
        f.write(unicharset_content)
    
    print("Custom unicharset created: binary_custom.unicharset")
    
    # Create font properties
    font_props = "binary_font 0 0 0 0 0\n"
    with open('binary_custom.font_properties', 'w') as f:
        f.write(font_props)
    
    print("Custom font properties created: binary_custom.font_properties")
    print("You can now use these files with Tesseract training tools.")

if __name__ == "__main__":
    print("Binary Pattern OCR Tool")
    print("=" * 40)
    
    # Create custom model files
    create_custom_binary_model()
    
    # Process images
    process_binary_images()
    
    print("\nProcessing complete!")
    print("Check the output files for OCR results.")