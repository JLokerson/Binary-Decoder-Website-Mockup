import subprocess
import os
import glob

def run_command(command):
    """Execute shell command and handle errors"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True

def train_tesseract_model():
    """Train custom Tesseract model for Gill Sans font"""
    
    # Check if tesseract training tools are installed
    if not run_command("tesseract --version"):
        print("Tesseract not found. Please install Tesseract OCR with training tools.")
        return
    
    # Create necessary directories
    os.makedirs("tessdata", exist_ok=True)
    
    # Step 1: Generate box files for each training image
    print("Step 1: Generating box files...")
    image_files = glob.glob("training_images/*.tif")
    
    for image_file in image_files:
        base_name = os.path.splitext(os.path.basename(image_file))[0]
        box_command = f'tesseract "{image_file}" "training_images/{base_name}" -l eng --psm 6 batch.nochop makebox'
        run_command(box_command)
    
    # Step 2: Create training files
    print("Step 2: Creating training files...")
    for image_file in image_files:
        base_name = os.path.splitext(os.path.basename(image_file))[0]
        
        # Generate .tr file
        tr_command = f'tesseract "training_images/{base_name}.tif" "training_images/{base_name}" -l eng --psm 6 box.train'
        run_command(tr_command)
    
    # Step 3: Extract character features
    print("Step 3: Extracting character features...")
    run_command("unicharset_extractor training_images/*.box")
    
    # Step 4: Create font properties file
    with open("font_properties", "w") as f:
        f.write("gillsans 0 0 0 0 0\n")
    
    # Step 5: Clustering
    print("Step 5: Clustering...")
    run_command("mftraining -F font_properties -U unicharset -O gillsans.unicharset training_images/*.tr")
    run_command("cntraining training_images/*.tr")
    
    # Step 6: Rename files
    print("Step 6: Renaming files...")
    files_to_rename = [
        ("inttemp", "gillsans.inttemp"),
        ("normproto", "gillsans.normproto"),
        ("pffmtable", "gillsans.pffmtable"),
        ("shapetable", "gillsans.shapetable")
    ]
    
    for old_name, new_name in files_to_rename:
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
    
    # Step 7: Combine data files
    print("Step 7: Combining data files...")
    run_command("combine_tessdata gillsans.")
    
    # Step 8: Move trained data to tessdata directory
    if os.path.exists("gillsans.traineddata"):
        os.rename("gillsans.traineddata", "tessdata/gillsans.traineddata")
        print("Training completed! gillsans.traineddata created in tessdata directory.")
    else:
        print("Training failed. gillsans.traineddata not created.")

if __name__ == "__main__":
    train_tesseract_model()
