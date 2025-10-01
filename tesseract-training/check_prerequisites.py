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
    print("\nDebugging font file detection:")
    
    # Check if training folder exists
    if not os.path.exists("training"):
        print("✗ Training folder does not exist")
        return False
    
    # List all files in training folder
    try:
        all_files = os.listdir("training")
        print(f"All files in training folder: {all_files}")
    except Exception as e:
        print(f"Error reading training folder: {e}")
        return False
    
    # Try multiple patterns to find OTF files
    otf_patterns = [
        "training/*.otf",
        "training/*.OTF",
        "training/*.[oO][tT][fF]"
    ]
    
    otf_files = []
    for pattern in otf_patterns:
        files = glob.glob(pattern)
        print(f"Pattern '{pattern}' found: {files}")
        otf_files.extend(files)
    
    # Remove duplicates
    otf_files = list(set(otf_files))
    
    # Also try manual detection
    manual_files = []
    try:
        for file in os.listdir("training"):
            if file.lower().endswith('.otf'):
                manual_files.append(os.path.join("training", file))
        print(f"Manual detection found: {manual_files}")
    except Exception as e:
        print(f"Manual detection error: {e}")
    
    # Combine results
    all_found = list(set(otf_files + manual_files))
    
    if all_found:
        print(f"✓ Font files found: {len(all_found)} OTF files in training folder")
        for font in all_found:
            print(f"  - {font}")
        return True
    else:
        print("✗ No OTF font files found in training folder")
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
