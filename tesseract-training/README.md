# Tesseract Gill Sans Font Training

This directory contains scripts to train a custom Tesseract model for better recognition of Gill Sans font.

## Prerequisites

1. Install Tesseract OCR with training tools:
   - Windows: Download from <https://github.com/UB-Mannheim/tesseract/wiki>
   - Make sure to include training tools in installation

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Place your Gill Sans font file in a `gill-sans/` subdirectory

## Usage

1. Generate training images:

   ```bash
   python generate_training_data.py
   ```

2. Train the model:

   ```bash
   python train_model.py
   ```

3. Test the trained model:

   ```bash
   python test_model.py
   ```

## Using the Trained Model

Once training is complete, you can use the custom model in your OCR code:

```python
import pytesseract
from PIL import Image

# Use custom Gill Sans model
custom_config = '--tessdata-dir "tessdata" -l gillsans --psm 6'
text = pytesseract.image_to_string(image, config=custom_config)
```

## Notes

- Training may take several minutes to complete
- The quality of training depends on the variety and quality of training text
- You may need to manually correct box files for better accuracy
