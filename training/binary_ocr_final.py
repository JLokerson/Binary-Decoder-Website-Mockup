#!/usr/bin/env python3
"""
Binary Pattern Recognition for Website
This script provides OCR functionality optimized for binary patterns in your website project.
"""

import subprocess
import sys
import os
import tempfile
import json

class BinaryOCR:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def recognize_binary_image(self, image_path):
        """
        Recognize binary patterns from an image
        Returns the recognized text and confidence
        """
        if not os.path.exists(image_path):
            return {"error": "Image file not found", "text": "", "confidence": 0}
        
        try:
            # Use the best approach we found: PSM 6 with character whitelist
            output_base = os.path.join(self.temp_dir, "ocr_result")
            
            cmd = [
                'tesseract', 
                image_path, 
                output_base,
                '--psm', '6',  # Uniform block of text
                '-c', 'tessedit_char_whitelist=01 ',  # Only allow 0, 1, and space
                '-c', 'preserve_interword_spaces=1'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Read the result
            result_file = f"{output_base}.txt"
            if os.path.exists(result_file):
                with open(result_file, 'r') as f:
                    text = f.read().strip()
                
                # Clean up the text - remove extra spaces and normalize
                cleaned_text = self.clean_binary_text(text)
                
                return {
                    "success": True,
                    "text": cleaned_text,
                    "raw_text": text,
                    "confidence": self.calculate_confidence(cleaned_text)
                }
            else:
                return {"error": "No OCR output generated", "text": "", "confidence": 0}
                
        except subprocess.CalledProcessError as e:
            return {"error": f"OCR failed: {e}", "text": "", "confidence": 0}
    
    def clean_binary_text(self, text):
        """
        Clean and normalize the OCR output for binary patterns
        """
        # Remove any characters that aren't 0, 1, space, or newline
        cleaned = ''.join(c for c in text if c in '01 \n\r\t')
        
        # Normalize spaces - replace multiple spaces with single space
        import re
        cleaned = re.sub(r' +', ' ', cleaned)
        
        # Clean up line breaks
        cleaned = re.sub(r'\n+', '\n', cleaned)
        
        return cleaned.strip()
    
    def calculate_confidence(self, text):
        """
        Calculate a simple confidence score based on the pattern
        """
        if not text:
            return 0
        
        # Count valid binary characters vs total characters
        binary_chars = sum(1 for c in text if c in '01')
        total_chars = len(text.replace(' ', '').replace('\n', ''))
        
        if total_chars == 0:
            return 0
        
        confidence = (binary_chars / total_chars) * 100
        return min(confidence, 100)  # Cap at 100%
    
    def batch_process(self, image_paths):
        """
        Process multiple images at once
        """
        results = {}
        for image_path in image_paths:
            results[image_path] = self.recognize_binary_image(image_path)
        return results
    
    def save_training_data(self, image_path, recognized_text, ground_truth=None):
        """
        Save recognition results for future training improvements
        """
        import datetime
        data = {
            "image_path": image_path,
            "recognized_text": recognized_text,
            "ground_truth": ground_truth,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        log_file = "binary_ocr_log.json"
        
        # Load existing log or create new
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                try:
                    log_data = json.load(f)
                except:
                    log_data = []
        else:
            log_data = []
        
        log_data.append(data)
        
        # Save updated log
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def cleanup(self):
        """
        Clean up temporary files
        """
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

def main():
    """
    Main function for command-line usage
    """
    if len(sys.argv) < 2:
        print("Usage: python binary_ocr_final.py <image_path>")
        print("Example: python binary_ocr_final.py IMG_2535.png")
        return
    
    image_path = sys.argv[1]
    
    # Create OCR instance
    ocr = BinaryOCR()
    
    # Process the image
    result = ocr.recognize_binary_image(image_path)
    
    # Display results
    print(f"Binary Pattern OCR Results for: {image_path}")
    print("=" * 50)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Confidence: {result['confidence']:.1f}%")
        print("\nRecognized Text:")
        print(result['text'])
        
        # Save the results
        ocr.save_training_data(image_path, result['text'])
        print(f"\nResults saved to binary_ocr_log.json")
    
    # Cleanup
    ocr.cleanup()

def test_all_images():
    """
    Test function to process all training images
    """
    images = ['IMG_2535.png', 'IMG_2542.png']
    ocr = BinaryOCR()
    
    print("Testing Binary OCR on all training images")
    print("=" * 50)
    
    for img in images:
        if os.path.exists(img):
            print(f"\nProcessing: {img}")
            result = ocr.recognize_binary_image(img)
            
            if "error" not in result:
                print(f"Confidence: {result['confidence']:.1f}%")
                print("Preview (first 100 chars):")
                preview = result['text'][:100] + "..." if len(result['text']) > 100 else result['text']
                print(preview)
                
                # Check against ground truth if available
                gt_file = img.replace('.png', '.gt.txt')
                if os.path.exists(gt_file):
                    with open(gt_file, 'r', encoding='utf-8') as f:
                        ground_truth = f.read().strip()
                    
                    # Save with ground truth
                    ocr.save_training_data(img, result['text'], ground_truth)
                    
                    # Simple accuracy check
                    if result['text'].replace(' ', '') == ground_truth.replace(' ', ''):
                        print("✓ Perfect match with ground truth!")
                    else:
                        print("✗ Different from ground truth")
                else:
                    ocr.save_training_data(img, result['text'])
            else:
                print(f"Error: {result['error']}")
    
    ocr.cleanup()
    print(f"\nAll results saved to binary_ocr_log.json")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        # Run test mode
        test_all_images()