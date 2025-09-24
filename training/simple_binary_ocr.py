#!/usr/bin/env python3
"""
Simple Binary Pattern OCR Tool for Tesseract
This script applies OCR with optimized settings for binary patterns.
"""

import subprocess
import sys
import os

def run_binary_ocr(image_path, output_base):
    """
    Run OCR with optimized settings for binary patterns
    """
    print(f"Running OCR on {image_path}...")
    
    # Try different approaches
    approaches = [
        {
            'name': 'Approach 1: PSM 6 with character whitelist',
            'cmd': [
                'tesseract', image_path, f"{output_base}_1",
                '--psm', '6',
                '-c', 'tessedit_char_whitelist=01 '
            ]
        },
        {
            'name': 'Approach 2: PSM 8 with character whitelist',
            'cmd': [
                'tesseract', image_path, f"{output_base}_2",
                '--psm', '8',
                '-c', 'tessedit_char_whitelist=01 '
            ]
        },
        {
            'name': 'Approach 3: PSM 7 with character whitelist',
            'cmd': [
                'tesseract', image_path, f"{output_base}_3",
                '--psm', '7',
                '-c', 'tessedit_char_whitelist=01 '
            ]
        },
        {
            'name': 'Approach 4: Default with character whitelist',
            'cmd': [
                'tesseract', image_path, f"{output_base}_4",
                '-c', 'tessedit_char_whitelist=01 '
            ]
        }
    ]
    
    results = {}
    
    for approach in approaches:
        try:
            print(f"\nTrying {approach['name']}...")
            result = subprocess.run(approach['cmd'], capture_output=True, text=True, check=True)
            
            # Read result
            result_file = f"{approach['cmd'][2]}.txt"
            if os.path.exists(result_file):
                with open(result_file, 'r') as f:
                    content = f.read().strip()
                results[approach['name']] = content
                print(f"Result: {content}")
            else:
                results[approach['name']] = "No output file generated"
                print("No output file generated")
                
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed: {e.stderr if e.stderr else str(e)}"
            results[approach['name']] = error_msg
            print(error_msg)
    
    return results

def compare_with_ground_truth(image_path, results):
    """
    Compare OCR results with ground truth if available
    """
    gt_file = image_path.replace('.png', '.gt.txt')
    if os.path.exists(gt_file):
        with open(gt_file, 'r') as f:
            ground_truth = f.read().strip()
        
        print(f"\nGround Truth for {image_path}:")
        print(ground_truth)
        print("\nComparison:")
        print("=" * 50)
        
        for approach, result in results.items():
            print(f"{approach}:")
            print(f"  Result: {result}")
            if result == ground_truth:
                print("  ✓ PERFECT MATCH!")
            else:
                print(f"  ✗ Different from ground truth")
            print()
    else:
        print(f"No ground truth file found: {gt_file}")

def process_images():
    """
    Process all images in the current directory
    """
    images = ['IMG_2535.png', 'IMG_2542.png']
    
    for img_file in images:
        if os.path.exists(img_file):
            print(f"\n{'='*60}")
            print(f"Processing {img_file}")
            print('='*60)
            
            output_base = img_file.replace('.png', '_result')
            results = run_binary_ocr(img_file, output_base)
            compare_with_ground_truth(img_file, results)
            
        else:
            print(f"Image file not found: {img_file}")

def create_simple_training_guide():
    """
    Create a guide for manual training
    """
    guide = """
# Manual Tesseract Training Guide for Binary Patterns

## Files you have:
- IMG_2535.png, IMG_2542.png (training images)
- IMG_2535.gt.txt, IMG_2542.gt.txt (ground truth text)
- Various training files (.box, .tr, .lstmf, etc.)

## Simple Training Approach:

1. Use existing English model as base:
   tesseract image.png output -l eng --psm 6 -c tessedit_char_whitelist=01

2. For better results, you can:
   - Improve image quality (increase contrast, size)
   - Use different PSM modes (6, 7, 8)
   - Fine-tune with LSTM training

## Current OCR Test Results:
Run this script to see how different approaches perform on your images.

## Next Steps:
If none of the approaches work well, consider:
1. Creating synthetic training data with different fonts
2. Using newer Tesseract versions (5.x)
3. Pre-processing images to improve quality
"""
    
    with open('training_guide.md', 'w') as f:
        f.write(guide)
    
    print("Training guide created: training_guide.md")

if __name__ == "__main__":
    print("Simple Binary Pattern OCR Tool")
    print("=" * 50)
    
    # Create training guide
    create_simple_training_guide()
    
    # Process images
    process_images()
    
    print(f"\n{'='*50}")
    print("Processing complete!")
    print("Check the output files and training_guide.md for more information.")