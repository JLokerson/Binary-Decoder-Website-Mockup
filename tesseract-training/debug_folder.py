import os
import sys

def debug_folder_access():
    """Debug folder access and file detection issues"""
    
    print("=== FOLDER DEBUG INFORMATION ===")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    print(f"OS: {os.name}")
    
    # Check training folder
    training_path = "training"
    abs_training_path = os.path.abspath(training_path)
    
    print(f"\nTraining folder path: {training_path}")
    print(f"Absolute training folder path: {abs_training_path}")
    print(f"Training folder exists: {os.path.exists(training_path)}")
    print(f"Training folder is directory: {os.path.isdir(training_path)}")
    
    # Check permissions
    if os.path.exists(training_path):
        print(f"Can read training folder: {os.access(training_path, os.R_OK)}")
        print(f"Can write to training folder: {os.access(training_path, os.W_OK)}")
        print(f"Can execute in training folder: {os.access(training_path, os.X_OK)}")
    
    # Try different ways to list files
    print(f"\n=== LISTING FILES IN TRAINING FOLDER ===")
    
    try:
        # Method 1: os.listdir
        files1 = os.listdir(training_path)
        print(f"os.listdir() result: {files1}")
    except Exception as e:
        print(f"os.listdir() error: {e}")
    
    try:
        # Method 2: os.scandir
        with os.scandir(training_path) as entries:
            files2 = [entry.name for entry in entries if entry.is_file()]
        print(f"os.scandir() files: {files2}")
    except Exception as e:
        print(f"os.scandir() error: {e}")
    
    try:
        # Method 3: os.walk
        for root, dirs, files in os.walk(training_path):
            print(f"os.walk() - root: {root}, files: {files}")
            break  # Only check first level
    except Exception as e:
        print(f"os.walk() error: {e}")
    
    # Check if there are hidden files
    try:
        import glob
        all_files = glob.glob(f"{training_path}/*")
        hidden_files = glob.glob(f"{training_path}/.*")
        print(f"glob all files: {all_files}")
        print(f"glob hidden files: {hidden_files}")
    except Exception as e:
        print(f"glob error: {e}")
    
    print(f"\n=== MANUAL PATH CHECK ===")
    # Check if user can manually navigate
    print("Please manually check:")
    print(f"1. Navigate to: {abs_training_path}")
    print("2. Verify OTF files are actually there")
    print("3. Check file names and extensions")
    print("4. Try running this script as administrator if needed")

if __name__ == "__main__":
    debug_folder_access()
