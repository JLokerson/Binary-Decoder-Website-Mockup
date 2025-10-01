import os
import glob

def setup_training_folder():
    """Create training folder and check for font files"""
    
    # Create training folder if it doesn't exist
    training_folder = "training"
    os.makedirs(training_folder, exist_ok=True)
    print(f"✓ Created/verified training folder: {training_folder}")
    
    # Debug: List all files in training folder
    print(f"\nDebugging - Contents of '{training_folder}' folder:")
    try:
        all_files = os.listdir(training_folder)
        if all_files:
            for file in all_files:
                file_path = os.path.join(training_folder, file)
                if os.path.isfile(file_path):
                    print(f"  - {file} (size: {os.path.getsize(file_path)} bytes)")
                else:
                    print(f"  - {file} (directory)")
        else:
            print("  (empty folder)")
    except Exception as e:
        print(f"  Error reading folder: {e}")
    
    # Check for OTF files more thoroughly
    otf_patterns = [
        f"{training_folder}/*.otf",
        f"{training_folder}/*.OTF", 
        f"{training_folder}/*.[oO][tT][fF]"
    ]
    
    otf_files = []
    for pattern in otf_patterns:
        files = glob.glob(pattern)
        otf_files.extend(files)
    
    # Remove duplicates
    otf_files = list(set(otf_files))
    
    if otf_files:
        print(f"\n✓ Found {len(otf_files)} OTF file(s):")
        for font in otf_files:
            print(f"  - {font}")
        print("\nYou can now run: python check_prerequisites.py")
    else:
        print(f"\n✗ No OTF files detected using glob patterns.")
        print("Trying manual file extension check...")
        
        # Manual check
        manual_otf_files = []
        try:
            for file in os.listdir(training_folder):
                if file.lower().endswith('.otf'):
                    manual_otf_files.append(os.path.join(training_folder, file))
            
            if manual_otf_files:
                print(f"✓ Manual check found {len(manual_otf_files)} OTF file(s):")
                for font in manual_otf_files:
                    print(f"  - {font}")
            else:
                print("Manual check also found no OTF files.")
                print("Please ensure your font files have .otf extension and are in the training folder.")
        except Exception as e:
            print(f"Error during manual check: {e}")

if __name__ == "__main__":
    setup_training_folder()
