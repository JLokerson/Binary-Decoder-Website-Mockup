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
    
    # Find OTF font files in training folder (check both locations)
    training_paths = ["training", "../training"]
    otf_files = []
    
    for training_path in training_paths:
        if os.path.exists(training_path):
            try:
                all_files = os.listdir(training_path)
                found_otf = [os.path.join(training_path, f) for f in all_files if f.lower().endswith('.otf')]
                otf_files.extend(found_otf)
                if found_otf:
                    break  # Use first location that has files
            except Exception as e:
                print(f"Error reading {training_path}: {e}")
    
    if not otf_files:
        print("No OTF font files found in training folders")
        print("Checked: training, ../training")
        return
    
    # Use the regular Gill Sans font (not bold, italic, etc.) for training
    font_path = None
    for font in otf_files:
        if "Gill Sans.otf" in font:  # Exact match for regular weight
            font_path = font
            break
    
    if not font_path:
        font_path = otf_files[0]  # Use first available if regular not found
    
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
