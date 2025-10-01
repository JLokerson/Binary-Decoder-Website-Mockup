import subprocess
import sys
import os
import glob

def check_command(command, description):
    """Check if a command exists and is working"""
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print(f"✓ {description}: Available")
        return True
    except Exception:
        print(f"✗ {description}: Not found or not working")
        return False

def check_python_packages():
    """Check required Python packages"""
    required_packages = ['PIL', 'pytesseract']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ Python package '{package}': Available")
        except ImportError:
            print(f"✗ Python package '{package}': Missing")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_font_files():
    """Check for OTF font files in training folder"""
    # Look in the training folder one level up
    training_paths = ["training", "../training"]
    
    for training_path in training_paths:
        if os.path.exists(training_path):
            try:
                all_files = os.listdir(training_path)
                otf_files = [f for f in all_files if f.lower().endswith('.otf')]
                
                if otf_files:
                    print(f"✓ Font files found: {len(otf_files)} OTF files in {os.path.abspath(training_path)}")
                    for font in otf_files[:5]:  # Show first 5 to avoid spam
                        print(f"  - {font}")
                    if len(otf_files) > 5:
                        print(f"  ... and {len(otf_files) - 5} more files")
                    return True
            except Exception as e:
                print(f"Error reading {training_path}: {e}")
    
    print("✗ No OTF font files found in training folder")
    print("  Checked paths: training, ../training")
    return False

def main():
    """Check all prerequisites for Tesseract training"""
    print("Checking Prerequisites for Tesseract Training")
    print("=" * 50)
    
    all_good = True
    
    # Check Tesseract
    if not check_command("tesseract --version", "Tesseract OCR"):
        all_good = False
        print("  Install from: https://github.com/UB-Mannheim/tesseract/wiki")
    
    # Check training tools
    training_tools = [
        ("unicharset_extractor --version", "unicharset_extractor"),
        ("mftraining -v", "mftraining"),
        ("cntraining -v", "cntraining"),
        ("combine_tessdata -v", "combine_tessdata")
    ]
    
    for cmd, tool in training_tools:
        if not check_command(cmd, f"Tesseract training tool '{tool}'"):
            all_good = False
    
    # Check Python packages
    if not check_python_packages():
        all_good = False
        print("  Install with: pip install Pillow pytesseract")
    
    # Check font files
    if not check_font_files():
        all_good = False
        print("  Place your Gill Sans OTF files in the 'training' folder")
    
    print("\n" + "=" * 50)
    if all_good:
        print("✓ All prerequisites met! You can proceed with training.")
        print("Run: python run_training.py")
    else:
        print("✗ Some prerequisites are missing. Please install them before training.")
    
    return all_good

if __name__ == "__main__":
    main()
