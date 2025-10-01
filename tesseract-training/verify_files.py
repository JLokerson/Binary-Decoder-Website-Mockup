import os

def verify_training_files():
    """Verify files are properly placed in training folder"""
    
    training_path = "training"
    abs_path = os.path.abspath(training_path)
    
    print(f"=== VERIFYING TRAINING FOLDER ===")
    print(f"Checking: {abs_path}")
    
    if not os.path.exists(training_path):
        print("❌ Training folder doesn't exist!")
        return False
    
    try:
        files = os.listdir(training_path)
        print(f"Files found: {len(files)}")
        
        if not files:
            print("❌ Training folder is empty!")
            print("Please copy your Gill Sans OTF files to this folder.")
            return False
        
        otf_files = []
        other_files = []
        
        for file in files:
            file_path = os.path.join(training_path, file)
            if os.path.isfile(file_path):
                if file.lower().endswith('.otf'):
                    otf_files.append(file)
                else:
                    other_files.append(file)
        
        print(f"\n=== FILE BREAKDOWN ===")
        if otf_files:
            print(f"✅ OTF files found: {len(otf_files)}")
            for font in otf_files:
                file_path = os.path.join(training_path, font)
                size = os.path.getsize(file_path)
                print(f"  - {font} ({size:,} bytes)")
        else:
            print("❌ No OTF files found!")
        
        if other_files:
            print(f"Other files: {len(other_files)}")
            for file in other_files:
                print(f"  - {file}")
        
        if otf_files:
            print(f"\n✅ Ready to proceed with training!")
            print(f"Run: python run_training.py")
            return True
        else:
            print(f"\n❌ No OTF files detected. Please add Gill Sans OTF files.")
            return False
            
    except Exception as e:
        print(f"Error checking files: {e}")
        return False

if __name__ == "__main__":
    verify_training_files()
