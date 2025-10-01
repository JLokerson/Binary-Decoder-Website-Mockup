import os
import shutil

def copy_model_to_web():
    """Copy the trained model to the web directory for browser use"""
    
    source_model = "tessdata/gillsans.traineddata"
    web_tessdata_dir = "../tessdata"
    target_model = os.path.join(web_tessdata_dir, "gillsans.traineddata")
    
    # Create web tessdata directory if it doesn't exist
    os.makedirs(web_tessdata_dir, exist_ok=True)
    
    if os.path.exists(source_model):
        try:
            shutil.copy2(source_model, target_model)
            print(f"✓ Model copied successfully!")
            print(f"  From: {os.path.abspath(source_model)}")
            print(f"  To: {os.path.abspath(target_model)}")
            print(f"\nYou can now use index-gillsans.html with the custom model.")
            
            # Check file size
            size = os.path.getsize(target_model)
            print(f"Model size: {size:,} bytes")
            
        except Exception as e:
            print(f"❌ Error copying model: {e}")
    else:
        print(f"❌ Source model not found: {source_model}")
        print("Make sure training completed successfully.")
        print("Check if tessdata/gillsans.traineddata exists in the training folder.")

if __name__ == "__main__":
    copy_model_to_web()
