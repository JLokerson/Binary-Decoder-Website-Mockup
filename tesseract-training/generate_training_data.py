import os
from PIL import Image, ImageDraw, ImageFont
import random
import glob

def generate_training_images():
    # Training text samples
    training_texts = [
        "The quick brown fox jumps over the lazy dog",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "!@#$%^&*()_+-=[]{}|;:,.<>?",
        "Binary code: 01101000 01100101 01101100 01101100 01101111",
        "Hexadecimal: 0x48656C6C6F",
        "Lorem ipsum dolor sit amet consectetur adipiscing elit"
    ]
    
    # Font settings
    font_sizes = [16, 20, 24, 28, 32]
    
    # Find OTF font files in training folder
    otf_files = glob.glob("training/*.otf")
    if not otf_files:
        print("No OTF font files found in training folder")
        return
    
    font_path = otf_files[0]  # Use first OTF file found
    print(f"Using font: {font_path}")
    
    os.makedirs("training_images", exist_ok=True)
    
    for i, text in enumerate(training_texts):
        for size in font_sizes:
            try:
                # Create image
                font = ImageFont.truetype(font_path, size)
                
                # Calculate image size
                bbox = font.getbbox(text)
                width = bbox[2] - bbox[0] + 40
                height = bbox[3] - bbox[1] + 40
                
                # Create white background image
                img = Image.new('RGB', (width, height), 'white')
                draw = ImageDraw.Draw(img)
                
                # Draw text in black
                draw.text((20, 20), text, font=font, fill='black')
                
                # Save image
                filename = f"gillsans.exp{i}.{size}.tif"
                img.save(f"training_images/{filename}")
                
                print(f"Generated: {filename}")
            except Exception as e:
                print(f"Error generating image with size {size}: {e}")

if __name__ == "__main__":
    generate_training_images()
