import subprocess
import sys
import os

def run_step(step_name, script_name):
    """Run a training step and handle errors"""
    print(f"\n{'='*50}")
    print(f"STEP: {step_name}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Warnings: {result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error in {step_name}:")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Script not found: {script_name}")
        return False

def main():
    """Run complete training pipeline"""
    print("Starting Tesseract Gill Sans Font Training Pipeline")
    
    # Check prerequisites
    if not os.path.exists("training"):
        print("Error: 'training' folder not found. Please ensure OTF font files are in the training folder.")
        return
    
    # Step 1: Generate training data
    if not run_step("Generate Training Images", "generate_training_data.py"):
        print("Failed to generate training images. Stopping.")
        return
    
    # Step 2: Train the model
    if not run_step("Train Tesseract Model", "train_model.py"):
        print("Failed to train model. Stopping.")
        return
    
    # Step 3: Test the model
    if not run_step("Test Trained Model", "test_model.py"):
        print("Failed to test model.")
        return
    
    print("\n" + "="*50)
    print("TRAINING COMPLETE!")
    print("="*50)
    print("Your custom Gill Sans model is ready to use.")
    print("Model location: tessdata/gillsans.traineddata")

if __name__ == "__main__":
    main()
