import pytesseract
from PIL import Image
import os

def test_trained_model():
    """Test the trained Gill Sans model"""
    
    # Set path to tessdata directory
    tessdata_dir = os.path.abspath("tessdata")
    
    # Configure pytesseract
    custom_config = f'--tessdata-dir "{tessdata_dir}" -l gillsans --psm 6'
    
    # Test with training images
    test_images = ["training_images/gillsans.exp0.24.tif"]  # Add more test images
    
    for image_path in test_images:
        if os.path.exists(image_path):
            print(f"\nTesting with: {image_path}")
            
            # Test with default English model
            text_eng = pytesseract.image_to_string(Image.open(image_path), lang='eng')
            print(f"Default English model result: {text_eng.strip()}")
            
            # Test with custom Gill Sans model
            try:
                text_custom = pytesseract.image_to_string(Image.open(image_path), config=custom_config)
                print(f"Custom Gill Sans model result: {text_custom.strip()}")
            except Exception as e:
                print(f"Error with custom model: {e}")
        else:
            print(f"Test image not found: {image_path}")

if __name__ == "__main__":
    test_trained_model()
