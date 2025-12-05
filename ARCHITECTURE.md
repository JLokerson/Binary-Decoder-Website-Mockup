# Binary Decoder - Technical Architecture

## 🏗️ System Architecture Overview

The Binary Decoder is a client-side web application built with vanilla JavaScript, HTML5, and CSS3. It processes binary code through multiple input methods and converts it to readable ASCII text.

## 📁 File Structure

```
z:\BinaryDecoder\
├── index.html              # Main menu/landing page
├── text-input.html         # Manual text input interface
├── take-photo.html         # Camera photo capture interface
├── insert-photo.html       # Image file upload interface
├── scan-camera.html        # Live camera scanning interface
├── style.css              # Global styles and responsive design
├── binary-decoder.js      # Core processing logic and OCR
├── binary-background.png  # Visual background pattern
├── package.json           # Project metadata and dependencies
├── generate-qr.js         # QR code generation utility
├── .github/workflows/deploy.yml  # CI/CD pipeline
├── README.md              # User documentation
└── ARCHITECTURE.md        # Technical documentation
```

## 🔧 Core Technologies

### Frontend Stack
- **HTML5**: Semantic markup, Canvas API, File API, Media API
- **CSS3**: Flexbox layouts, CSS Grid, gradients, animations
- **Vanilla JavaScript**: ES6+ features, async/await, modules
- **Web APIs**: getUserMedia, FileReader, Canvas 2D Context

### External Libraries
- **Tesseract.js v5**: WebAssembly-based OCR engine
- **QRCode (Node.js)**: QR code generation for sharing

### Development Tools
- **http-server**: Local development server
- **gh-pages**: GitHub Pages deployment
- **GitHub Actions**: Automated CI/CD pipeline

## 🎯 Core Processing Pipeline

### 1. Input Acquisition Layer
```javascript
// Text Input
textarea.oninput → binaryToAscii() → display result

// Camera Capture  
getUserMedia() → canvas.drawImage() → OCR processing

// File Upload
FileReader.readAsDataURL() → img.onload → OCR processing

// Live Scanning
setInterval() → frame capture → OCR processing
```

### 2. Image Processing Layer
```javascript
// Canvas preprocessing for OCR optimization
function preprocessCanvas(canvas) {
    const ctx = canvas.getContext('2d');
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    
    // Convert to grayscale for better OCR accuracy
    for (let i = 0; i < imageData.data.length; i += 4) {
        let avg = (imageData.data[i] + imageData.data[i+1] + imageData.data[i+2]) / 3;
        imageData.data[i] = imageData.data[i+1] = imageData.data[i+2] = avg;
    }
    
    ctx.putImageData(imageData, 0, 0);
}
```

### 3. OCR Processing Layer
```javascript
// Tesseract.js integration with worker management
async function performOCR(imageDataUrl) {
    if (!tesseractWorker) {
        tesseractWorker = await loadCustomModel();
    }
    
    const { data: { text } } = await tesseractWorker.recognize(imageDataUrl);
    return binaryToAscii(text);
}
```

### 4. Binary Conversion Layer
```javascript
// Multi-step binary processing with error correction
function binaryToAscii(binaryStr) {
    // Step 1: OCR error correction
    let cleaned = binaryStr
        .replace(/[lI|!]/g, '1')      // Common OCR mistakes → 1
        .replace(/[OoQD\[\]]/g, '0')  // Common OCR mistakes → 0
        .replace(/[^01\s]/g, '')      // Remove non-binary chars
        .replace(/\s+/g, ' ')         // Normalize whitespace
        .trim();
    
    // Step 2: Extract valid 8-bit groups
    const words = cleaned.split(/\s+/);
    const validBinaries = words.filter(w => w.length === 8 && /^[01]{8}$/.test(w));
    
    // Step 3: Convert to ASCII
    return validBinaries.map(bin => String.fromCharCode(parseInt(bin, 2))).join('');
}
```

## 🎨 UI/UX Architecture

### Design System
```css
/* Color Palette */
:root {
    --primary-orange: #F56600;      /* Interactive elements */
    --background-gradient: linear-gradient(to bottom, #A8A8A8 0%, #4e4e4e 100%);
    --text-white: #FFFFFF;          /* Headers and labels */
    --text-black: #000000;          /* Content and results */
    --surface-white: #FFFFFF;       /* Cards and containers */
}

/* Responsive Breakpoints */
@media (max-width: 900px) { /* Mobile optimizations */ }
@media (min-width: 901px) { /* Desktop enhancements */ }
```

### Component Architecture
1. **Header Component**: Consistent branding across pages
2. **Description Cards**: Informational content with black text on white
3. **Button System**: Orange-themed interactive elements
4. **Output Areas**: Standardized result display containers
5. **Camera Components**: Video feeds with consistent sizing

## 📱 Responsive Design Strategy

### Mobile-First Approach
```css
/* Base styles: Mobile default */
.container {
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
}

/* Progressive enhancement for larger screens */
@media (min-width: 901px) {
    .container {
        max-width: 400px;
    }
}
```

### Touch Optimization
- **Minimum touch targets**: 44px height for accessibility
- **Button spacing**: 15px gaps between interactive elements  
- **Gesture support**: Pinch-to-zoom disabled for consistent experience
- **Orientation handling**: Layout adapts to portrait/landscape

## 🔐 Security Implementation

### Camera Access Security
```javascript
async function requestCamera() {
    // Validate secure context (HTTPS or localhost)
    const isSecureContext = window.isSecureContext || 
                           location.protocol === 'https:' || 
                           location.hostname === 'localhost' ||
                           location.hostname === '127.0.0.1';
    
    if (!isSecureContext) {
        throw new Error('Camera access requires HTTPS or localhost');
    }
    
    // Request with environment preference, fallback to any camera
    try {
        return await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: "environment" } 
        });
    } catch (err) {
        return await navigator.mediaDevices.getUserMedia({ video: true });
    }
}
```

### Privacy Protection
- **Camera streams**: Automatically stopped after use
- **File processing**: Client-side only, no server uploads
- **OCR processing**: Local WebAssembly execution
- **Data retention**: No persistent storage of user content

## ⚡ Performance Optimization

### OCR Worker Management
```javascript
// Singleton worker pattern for efficiency
let tesseractWorker = null;

async function loadCustomModel() {
    if (!tesseractWorker) {
        tesseractWorker = await Tesseract.createWorker('eng', 1, {
            logger: m => console.log(m)  // Development logging
        });
    }
    return tesseractWorker;
}
```

### Image Processing Optimization
- **Scale factor**: 2x resolution for OCR accuracy vs performance balance
- **Canvas reuse**: Single canvas element per page to reduce memory
- **Preprocessing**: Grayscale conversion reduces processing complexity
- **Frame rate limiting**: 1-second intervals for live scanning

### Resource Loading
- **Lazy initialization**: Tesseract worker loaded on first use
- **CDN delivery**: External libraries served from reliable CDNs  
- **Asset optimization**: Compressed images and minified scripts
- **Caching strategy**: Browser caching for static assets

## 🧪 Testing Strategy

### Browser Compatibility Testing
- **Modern browsers**: Chrome 60+, Firefox 55+, Safari 11+, Edge 79+
- **Mobile browsers**: iOS Safari 11+, Chrome Mobile 60+
- **Feature detection**: Graceful degradation for unsupported features

### OCR Accuracy Testing
```javascript
// Test patterns for validation
const testBinary = "01001000 01100101 01101100 01101100 01101111"; // "Hello"
const expectedResult = "Hello";
const actualResult = binaryToAscii(testBinary);
console.assert(actualResult === expectedResult, 'Binary conversion test failed');
```

### Camera Integration Testing
- **Permission handling**: User denial scenarios
- **Device compatibility**: Front/rear camera availability
- **Error recovery**: Network issues and timeout handling

## 🚀 Deployment Architecture

### CI/CD Pipeline
```yaml
# GitHub Actions workflow
name: Deploy to GitHub Pages
on:
  push:
    branches: [ main ]
    
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    - name: Install dependencies
      run: npm install
    - name: Build project  
      run: npm run build
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
```

### Production Environment
- **Static hosting**: GitHub Pages with custom domain support
- **HTTPS enforcement**: Required for camera API functionality
- **CDN integration**: External libraries served via CDN
- **Monitoring**: Error tracking and performance monitoring

## 🔄 Data Flow Diagram

```
User Input
    ↓
[Input Method Selection]
    ↓
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Text Input  │ Photo Capture│ File Upload │ Live Scan   │
└─────────────┴─────────────┴─────────────┴─────────────┘
    ↓               ↓               ↓               ↓
Direct Processing   Camera API    File Reader    Video Stream
    ↓               ↓               ↓               ↓
binaryToAscii()    Canvas Draw   Canvas Draw   Canvas Draw
    ↓               ↓               ↓               ↓
ASCII Output   → OCR Process → OCR Process → OCR Process
                    ↓               ↓               ↓
               binaryToAscii() binaryToAscii() binaryToAscii()
                    ↓               ↓               ↓
               ASCII Output    ASCII Output    ASCII Output
```

## 🛠️ Extension Points

### Adding New Input Methods
1. Create new HTML page following existing pattern
2. Implement input-specific logic in JavaScript
3. Integrate with existing `binaryToAscii()` function
4. Add navigation link to main menu

### OCR Engine Alternatives
```javascript
// Modular OCR interface for easy swapping
async function performOCR(imageDataUrl, engine = 'tesseract') {
    switch(engine) {
        case 'tesseract':
            return await tesseractOCR(imageDataUrl);
        case 'cloud-vision':
            return await cloudVisionOCR(imageDataUrl);
        default:
            throw new Error('Unsupported OCR engine');
    }
}
```

### Additional Output Formats
- **Hexadecimal conversion**: Binary → Hex display
- **Decimal conversion**: Binary → Decimal values  
- **Export functionality**: Save results to file
- **History tracking**: Store previous conversions
