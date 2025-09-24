
# Manual Tesseract Training Guide for Binary Patterns

## Files you have:
- IMG_2535.png, IMG_2542.png (training images)
- IMG_2535.gt.txt, IMG_2542.gt.txt (ground truth text)
- Various training files (.box, .tr, .lstmf, etc.)

## Simple Training Approach:

1. Use existing English model as base:
   tesseract image.png output -l eng --psm 6 -c tessedit_char_whitelist=01

2. For better results, you can:
   - Improve image quality (increase contrast, size)
   - Use different PSM modes (6, 7, 8)
   - Fine-tune with LSTM training

## Current OCR Test Results:
Run this script to see how different approaches perform on your images.

## Next Steps:
If none of the approaches work well, consider:
1. Creating synthetic training data with different fonts
2. Using newer Tesseract versions (5.x)
3. Pre-processing images to improve quality
