# Binary Decoder Website Documentation

A versatile web application that converts binary code to ASCII text using multiple input methods including camera scanning, image upload, and direct text input.

## 🌐 Live Demo
Visit the deployed application: [Binary Decoder](https://wfic-util-01.clemson.edu/decoder/)

## 📱 Features
- **Real-time binary decoding** from multiple input sources
- **Camera integration** for live scanning and photo capture
- **OCR technology** using Tesseract.js for image-to-text conversion
- **Mobile-responsive design** optimized for all devices
- **Secure HTTPS** camera access with localhost fallback

## 📄 Page Documentation

### 🏠 index.html - Main Menu Page
**Purpose**: Landing page that provides navigation to all decoder methods.

**Features**:
- Animated binary background pattern for visual appeal
- Four main navigation options with large, accessible buttons
- Responsive design that adapts to mobile and desktop
- Clean, professional interface with orange accent colors

**How it works**:
1. Displays welcome message and feature overview
2. Shows four input method options as large buttons
3. Each button navigates to a specialized decoder page
4. Background generates dynamic binary pattern on load

**Technical details**:
- Uses CSS gradients for background styling
- Implements responsive button layout with flexbox
- Loads binary background image with CSS fallback
- Preloads Tesseract.js OCR engine for faster subsequent pages

---

### ⌨️ text-input.html - Direct Text Input Page
**Purpose**: Allows users to manually type or paste binary code for real-time decoding.

**Features**:
- Large text area for binary input with monospace font
- Real-time decoding as user types
- Supports 8-bit binary groups separated by spaces
- Helpful input format tips and validation

**How it works**:
1. User enters binary code in the textarea (e.g., "01001000 01100101")
2. JavaScript listens for input events and triggers decoding
3. Binary groups are validated and converted to ASCII characters
4. Results display instantly in the output area

**Input format**:
- Accepts binary in 8-bit groups: `01001000 01100101 01101100`
- Automatically filters non-binary characters
- Corrects common OCR mistakes (I→1, O→0, etc.)
- Requires space separation between 8-bit groups for optimal parsing

**Technical implementation**:
- Uses `oninput` event listener for real-time processing
- Calls `binaryToAscii()` function from binary-decoder.js
- Validates input format before attempting conversion
- Provides user feedback for invalid input patterns

---

### 📷 take-photo.html - Camera Photo Capture Page
**Purpose**: Captures photos using device camera and extracts binary code via OCR.

**Features**:
- Camera access with environment (rear) camera preference
- Photo capture with automatic OCR processing
- HTTPS/localhost security requirement handling
- Mobile and desktop camera support

**How it works**:
1. Click "Start Camera" to request camera permissions
2. Camera feed displays in video element (320x240px)
3. Click "Capture Photo" to take a snapshot
4. Photo is automatically processed through Tesseract OCR
5. Extracted text is decoded from binary to ASCII

**Security requirements**:
- Requires HTTPS or localhost for camera access
- Graceful fallback to front camera if rear unavailable
- Clear error messages for permission denials
- Stops camera stream after capture to preserve privacy

**Processing pipeline**:
1. Canvas captures current video frame at 2x resolution
2. Image preprocessing applies grayscale conversion
3. Tesseract OCR extracts text from processed image
4. Binary decoder converts OCR results to ASCII text

---

### 🖼️ insert-photo.html - Image Upload Page  
**Purpose**: Processes uploaded image files to extract and decode binary code.

**Features**:
- File input dialog for image selection
- Image preview before processing
- Automatic OCR and binary decoding
- Support for common image formats (PNG, JPG, etc.)

**How it works**:
1. Click "Select Image File" to open file dialog
2. Choose image containing binary code text
3. Image displays as preview in 320x240px container
4. OCR automatically processes the uploaded image
5. Binary text is extracted and converted to ASCII

**Image processing**:
- Creates temporary canvas for OCR processing at 2x scale
- Applies grayscale preprocessing for better OCR accuracy
- Uses Tesseract.js with English language model
- Handles various image formats through HTML5 File API

**User feedback**:
- Shows upload status during processing
- Displays selected image for verification
- Button text changes to "Select Different Image" after upload
- Clear error messages for processing failures

---

### 📡 scan-camera.html - Live Camera Scanning Page
**Purpose**: Provides continuous real-time scanning of binary code through camera feed.

**Features**:
- Live camera feed with continuous OCR scanning
- Real-time binary detection and decoding
- Start/stop controls for scanning session
- Optimized for detecting binary code in camera view

**How it works**:
1. Click "Start Live Scan" to activate camera
2. Camera feed begins and OCR scanning starts automatically
3. System captures frames every 1000ms (1 second intervals)
4. Each frame is processed through OCR and binary decoder
5. Results update in real-time as binary code is detected

**Scanning process**:
- Extracts 640x640 square region from center of camera feed
- Processes frames at regular intervals to balance performance
- Applies image preprocessing for optimal OCR results
- Continuously updates decoded text output

**Performance optimization**:
- 1-second intervals prevent excessive processing
- Square crop focuses on center area of camera view
- Grayscale conversion improves OCR accuracy
- Automatic cleanup of camera resources when stopped

---

## 🛠️ Core JavaScript Functions

### binary-decoder.js - Main Processing Engine

#### `binaryToAscii(binaryStr, printableOnly = false)`
Converts binary string to ASCII text with OCR error correction.

**Parameters**:
- `binaryStr`: Input binary string (may contain spaces and OCR errors)
- `printableOnly`: Filter to only printable ASCII characters (32-126)

**Error correction**:
- Converts common OCR mistakes: `l,I,|,!` → `1` and `O,o,Q,D,[,]` → `0`
- Handles mixed case and special character substitutions
- Filters non-binary characters and normalizes spacing

**Process**:
1. Apply OCR corrections to convert similar-looking characters
2. Remove non-binary characters and normalize whitespace
3. Split into words and validate 8-bit binary groups
4. Convert each valid binary group to ASCII character
5. Optionally filter to printable characters only

#### `performOCR(imageDataUrl)`
Processes images through Tesseract OCR engine for text extraction.

**Process**:
1. Initialize Tesseract worker if not already loaded
2. Process image data URL through OCR recognition
3. Normalize extracted text by removing extra whitespace
4. Apply binary conversion with error correction
5. Return decoded ASCII text or error message

#### `generateBinaryBackground()`
Creates animated binary pattern background with image and CSS fallbacks.

**Implementation**:
1. Attempts to load binary-background.png image
2. On success: applies repeating background pattern
3. On failure: generates CSS-based fallback pattern
4. Adjusts opacity and sizing for mobile vs desktop
5. Handles orientation changes and visibility events

## 📱 Mobile Responsiveness

### Responsive Design Features
- **Breakpoint**: 900px width for mobile/desktop distinction
- **Header scaling**: Reduced height and font size on mobile
- **Button optimization**: Full-width buttons with larger touch targets
- **Camera sizing**: Fixed dimensions that work across devices
- **Text scaling**: Adjusted font sizes for readability

### Mobile-specific Optimizations
- **Camera handling**: Prefers rear camera, falls back gracefully
- **Touch targets**: Minimum 44px height for accessibility
- **Viewport handling**: Proper scaling and zoom prevention
- **Performance**: Optimized OCR intervals and image processing

## 🔧 Technical Architecture

### Dependencies
- **Tesseract.js v5**: OCR engine for image-to-text conversion
- **HTML5 APIs**: Camera access, File API, Canvas processing
- **CSS3**: Gradients, flexbox, responsive design
- **Vanilla JavaScript**: No external frameworks for maximum compatibility

### Security Considerations
- **HTTPS requirement** for camera access in production
- **Localhost exception** for development environments
- **Permission handling** with graceful error recovery
- **Privacy protection** by stopping camera streams after use

### Performance Features
- **Lazy loading**: Tesseract worker loaded on demand
- **Preprocessing**: Image optimization before OCR processing
- **Caching**: Reuse of OCR worker across multiple operations
- **Debouncing**: Controlled intervals for live scanning

## 🚀 Deployment

### GitHub Pages Deployment
- Automated deployment via GitHub Actions
- Static file hosting with HTTPS support
- Custom domain configuration available
- Continuous deployment from main branch

### Local Development
```bash
npm install          # Install dependencies
npm start           # Start local server on port 3000
npm run generate-qr # Generate QR codes for sharing
```

### Production Setup
- Ensure HTTPS for camera functionality
- Configure proper MIME types for static assets
- Set up CDN for Tesseract.js if needed
- Monitor performance and error logging

## 📊 Browser Compatibility
- **Modern browsers**: Chrome 60+, Firefox 55+, Safari 11+, Edge 79+
- **Camera support**: Requires getUserMedia API
- **OCR processing**: WebAssembly support required for Tesseract
- **Mobile browsers**: iOS Safari 11+, Chrome Mobile 60+

## 🔍 Troubleshooting

### Common Issues
1. **Camera not working**: Check HTTPS/localhost requirement
2. **OCR accuracy**: Ensure good lighting and clear binary text
3. **Mobile performance**: Reduce image resolution if processing is slow
4. **File upload limits**: Browser may limit large image files

### Debug Information
- Console logging for OCR results and processing steps
- Error messages displayed to users for failed operations
- Network tab shows Tesseract.js loading progress
- Camera permissions visible in browser security indicators
