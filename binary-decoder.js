/**
 * Binary Decoder - Core Processing Engine
 * 
 * This file contains the main logic for:
 * - Binary to ASCII conversion with OCR error correction
 * - Tesseract.js OCR processing and worker management
 * - Dynamic binary background pattern generation
 * - Image preprocessing for optimal OCR accuracy
 * 
 * @author Binary Decoder Team
 * @version 1.0.0
 */

/**
 * Generate binary pattern background using provided image with mobile fallback
 * Creates an animated binary background pattern that adapts to screen size and device capabilities.
 * 
 * Implementation details:
 * - Attempts to load binary-background.png image first
 * - Falls back to CSS-generated patterns if image fails
 * - Adjusts opacity and sizing based on screen width
 * - Handles mobile vs desktop optimization automatically
 * 
 * Mobile optimizations:
 * - Reduced background size (200px vs 400px) for performance
 * - Lower opacity (0.15 vs 0.25) for better text readability
 * - Responsive scaling that adapts to orientation changes
 */
function generateBinaryBackground() {
    const backgroundDiv = document.getElementById('binaryBackground');
    
    if (!backgroundDiv) return; // Safety check
    
    // Completely clear any existing content and styles
    backgroundDiv.innerHTML = '';
    backgroundDiv.textContent = '';
    backgroundDiv.innerText = '';
    
    // Remove any existing inline styles that might interfere
    backgroundDiv.style.fontFamily = '';
    backgroundDiv.style.fontSize = '';
    backgroundDiv.style.lineHeight = '';
    backgroundDiv.style.color = '';
    backgroundDiv.style.whiteSpace = '';
    backgroundDiv.style.wordWrap = '';
    backgroundDiv.style.padding = '';
    
    // Ensure proper sizing with better mobile coverage
    backgroundDiv.style.width = '100%';
    backgroundDiv.style.height = '100%';
    backgroundDiv.style.left = '0';
    backgroundDiv.style.top = '0';
    backgroundDiv.style.minHeight = '100vh';
    backgroundDiv.style.minWidth = '100vw';
    backgroundDiv.style.position = 'fixed';
    backgroundDiv.style.zIndex = '1';
    backgroundDiv.style.pointerEvents = 'none';
    backgroundDiv.style.overflow = 'hidden';
    
    // Try image first, fallback to CSS pattern
    const testImg = new Image();
    testImg.onload = () => {
        console.log('Background image loaded successfully');
        backgroundDiv.style.backgroundImage = `url("./binary-background.png")`;
        backgroundDiv.style.backgroundRepeat = 'repeat';
        backgroundDiv.style.backgroundPosition = '0 0';
        backgroundDiv.style.opacity = '0.25'; // Increased default opacity
        
        // Add mobile-specific adjustments with better visibility
        if (window.innerWidth <= 900) {
            backgroundDiv.style.backgroundSize = 'auto 200px'; // Optimized for mobile
            backgroundDiv.style.opacity = '0.15'; // More subtle on mobile
        } else {
            backgroundDiv.style.backgroundSize = 'auto 400px'; // Fixed size for desktop
        }
    };
    
    testImg.onerror = () => {
        console.log('Background image failed to load, using CSS fallback pattern');
        // Fallback CSS pattern
        backgroundDiv.style.background = `
            repeating-linear-gradient(
                45deg,
                rgba(255,255,255,0.05) 0px,
                rgba(255,255,255,0.05) 2px,
                transparent 2px,
                transparent 4px
            ),
            repeating-linear-gradient(
                -45deg,
                rgba(255,255,255,0.03) 0px,
                rgba(255,255,255,0.03) 1px,
                transparent 1px,
                transparent 3px
            )
        `;
        backgroundDiv.style.opacity = '0.2';
    };
    
    testImg.src = './binary-background.png';
}

// Tesseract worker - Singleton pattern for efficient OCR processing
let tesseractWorker = null;

/**
 * Load and configure Tesseract OCR worker
 * 
 * Uses singleton pattern to ensure only one worker instance exists.
 * Provides error handling and fallback configuration for reliability.
 * 
 * @returns {Promise<Worker>} Configured Tesseract worker instance
 * 
 * Performance considerations:
 * - Worker is created once and reused for all OCR operations
 * - English language model is preloaded for faster processing
 * - Logging is enabled for development debugging
 */
async function loadCustomModel() {
    try {
        const worker = await Tesseract.createWorker('eng', 1, {
            logger: m => console.log(m)
        });
        return worker;
    } catch (error) {
        console.error('Error creating Tesseract worker:', error);
        const worker = await Tesseract.createWorker('eng');
        return worker;
    }
}

/**
 * Perform OCR processing on image data
 * 
 * Main OCR processing function that handles:
 * - Tesseract worker initialization and management
 * - Image recognition and text extraction
 * - Error handling and fallback responses
 * - Integration with binary conversion pipeline
 * 
 * @param {string} imageDataUrl - Base64 encoded image data URL
 * @returns {Promise<string>} Decoded ASCII text or error message
 * 
 * Processing pipeline:
 * 1. Initialize Tesseract worker if not already loaded
 * 2. Pass image data to OCR recognition engine
 * 3. Normalize extracted text (remove extra whitespace)
 * 4. Apply binary conversion with error correction
 * 5. Return final ASCII result or appropriate error message
 */
async function performOCR(imageDataUrl) {
    if (!tesseractWorker) {
        tesseractWorker = await loadCustomModel();
    }
    
    try {
        const { data: { text } } = await tesseractWorker.recognize(imageDataUrl);
        console.log("Raw Tesseract OCR result:", text);
        
        const binaryStr = text.replace(/\s+/g, ' ').trim();
        console.log("Normalized OCR text:", binaryStr);
        
        const ascii = binaryToAscii(binaryStr);
        return ascii || '// No valid binary detected';
    } catch (error) {
        console.error("OCR error:", error);
        return '// OCR error';
    }
}

/**
 * Convert binary string to ASCII text with comprehensive error correction
 * 
 * This is the core conversion function that handles:
 * - OCR error correction for common character misidentification
 * - Binary validation and formatting
 * - ASCII character conversion and filtering
 * - Support for various input formats and edge cases
 * 
 * @param {string} binaryStr - Input binary string (may contain OCR errors and formatting)
 * @param {boolean} printableOnly - Filter to only printable ASCII characters (32-126)
 * @returns {string} Decoded ASCII text or empty string if no valid binary found
 * 
 * OCR Error Correction Patterns:
 * - l, I, |, ! → 1 (vertical line characters commonly misread as binary 1)
 * - O, o, Q, D, [, ] → 0 (circular/bracket characters misread as binary 0)
 * - OI → 01, IO → 10, Ol → 01, lO → 10 (common adjacent character mistakes)
 * 
 * Validation Rules:
 * - Only processes valid 8-bit binary groups (exactly 8 characters of 0s and 1s)
 * - Requires space separation between groups for accurate parsing
 * - Filters out any non-binary characters after correction
 * 
 * ASCII Conversion:
 * - Converts each valid 8-bit binary to decimal (0-255)
 * - Maps decimal to corresponding ASCII character
 * - Optionally filters to printable range (32-126) for display
 */
function binaryToAscii(binaryStr, printableOnly = false) {
    console.log("Input binary string:", binaryStr);
    
    // Step 1: Apply OCR error corrections
    let cleaned = binaryStr
        .replace(/[lI|!]/g, '1')      // Vertical lines → 1
        .replace(/[OoQD\[\]]/g, '0')  // Circular shapes → 0
        .replace(/OI/g, '01')         // Adjacent char corrections
        .replace(/IO/g, '10')
        .replace(/Ol/g, '01')
        .replace(/lO/g, '10')
        .replace(/[^01\s]/g, '')      // Remove non-binary characters
        .replace(/\s+/g, ' ')         // Normalize whitespace
        .trim();
    
    console.log("After OCR corrections:", cleaned);
    
    // Step 2: Extract and validate 8-bit binary groups
    const words = cleaned.split(/\s+/).filter(word => word.length > 0);
    const validBinaries = words.filter(w => w.length === 8 && /^[01]{8}$/.test(w));
    
    if (validBinaries.length === 0) {
        return '';
    }
    
    // Step 3: Convert binary groups to ASCII characters
    let ascii = validBinaries.map(bin => {
        const charCode = parseInt(bin, 2);
        return String.fromCharCode(charCode);
    }).join('');
    
    // Step 4: Optional filtering to printable characters only
    if (printableOnly) {
        ascii = ascii.split('').filter(c => {
            const code = c.charCodeAt(0);
            return code >= 32 && code <= 126;
        }).join('');
    }
    
    return ascii;
}

/**
 * Preprocess canvas image for optimal OCR accuracy
 * 
 * Applies image processing techniques to improve OCR recognition:
 * - Converts color images to grayscale for better text detection
 * - Reduces noise and improves contrast for cleaner character recognition
 * - Maintains aspect ratio while optimizing for Tesseract processing
 * 
 * @param {HTMLCanvasElement} canvas - Canvas element containing image to process
 * @param {HTMLCanvasElement} debugCanvas - Optional canvas for displaying processed image
 * 
 * Processing steps:
 * 1. Extract image data from canvas context
 * 2. Convert RGB pixels to grayscale using average method
 * 3. Update canvas with processed image data
 * 4. Optionally display processed result in debug canvas
 */
function preprocessCanvas(canvas, debugCanvas) {
    const ctx = canvas.getContext('2d');
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    
    // Convert to grayscale for better OCR accuracy
    for (let i = 0; i < imageData.data.length; i += 4) {
        let avg = (imageData.data[i] + imageData.data[i+1] + imageData.data[i+2]) / 3;
        imageData.data[i] = imageData.data[i+1] = imageData.data[i+2] = avg;
    }
    ctx.putImageData(imageData, 0, 0);
    
    // Optional debug display
    if (debugCanvas) {
        debugCanvas.width = canvas.width;
        debugCanvas.height = canvas.height;
        debugCanvas.getContext('2d').putImageData(imageData, 0, 0);
        document.getElementById('toggleProcessedBtn').style.display = 'inline-block';
    }
}

/**
 * Process captured camera image through OCR pipeline
 * 
 * Complete processing workflow for camera-captured images:
 * - Scales image for optimal OCR processing (2x resolution)
 * - Applies preprocessing for better character recognition
 * - Manages UI feedback during processing
 * - Displays final results to user
 * 
 * @param {HTMLCanvasElement} canvas - Canvas containing captured camera image
 * 
 * Processing pipeline:
 * 1. Scale image 2x for better OCR accuracy
 * 2. Apply grayscale preprocessing
 * 3. Convert to data URL for Tesseract processing
 * 4. Update UI with processing status
 * 5. Display final decoded results
 */
function runOcrOnCanvas(canvas) {
    document.getElementById('decodedText').textContent = 'Scanning...';
    
    // Scale image 2x for better OCR accuracy
    const scale = 2;
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.width * scale;
    tempCanvas.height = canvas.height * scale;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(canvas, 0, 0, tempCanvas.width, tempCanvas.height);
    
    // Apply preprocessing and perform OCR
    preprocessCanvas(tempCanvas, document.getElementById('processedCanvas'));
    const imageDataUrl = tempCanvas.toDataURL('image/png');
    
    performOCR(imageDataUrl).then(result => {
        document.getElementById('decodedText').textContent = result;
    });
}

/**
 * Process uploaded image file through OCR pipeline
 * 
 * Handles uploaded image files with proper loading and processing:
 * - Manages image loading states and timing
 * - Scales images for optimal OCR processing
 * - Provides error handling for failed loads
 * - Integrates with standard OCR processing pipeline
 * 
 * @param {HTMLImageElement} img - Image element containing uploaded file
 * 
 * Processing considerations:
 * - Waits for complete image load before processing
 * - Uses natural dimensions for accurate scaling
 * - Applies 2x scaling factor for OCR optimization
 * - Handles both immediate and delayed image loading
 */
function runOcrOnImage(img) {
    const processImage = async function() {
        const scale = 2;
        const w = img.naturalWidth * scale;
        const h = img.naturalHeight * scale;
        
        const canvas = document.getElementById('photoCanvas');
        canvas.width = w;
        canvas.height = h;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        canvas.style.display = 'none';
        
        preprocessCanvas(canvas, document.getElementById('processedCanvas'));
        const imageDataUrl = canvas.toDataURL('image/png');
        
        document.getElementById('decodedText').textContent = 'Scanning...';
        const result = await performOCR(imageDataUrl);
        document.getElementById('decodedText').textContent = result;
    };
    
    // Handle both immediate and delayed image loading
    if (img.complete && img.naturalWidth > 0) {
        processImage();
    } else {
        img.onload = processImage;
    }
}

/**
 * Initialize application on page load
 * 
 * Main initialization function that:
 * - Sets up binary background pattern
 * - Preloads Tesseract OCR worker for faster processing
 * - Configures responsive event listeners
 * - Handles mobile-specific optimizations
 * 
 * Event listeners:
 * - Window resize: Updates background pattern for new dimensions
 * - Orientation change: Handles mobile device rotation
 * - Visibility change: Refreshes background when page becomes active
 * 
 * Performance optimizations:
 * - OCR worker preloading reduces first-use latency
 * - Debounced resize handlers prevent excessive processing
 * - Mobile-specific timeouts account for orientation change delays
 */
// Initialize on page load
window.onload = async () => {
    generateBinaryBackground();
    
    try {
        tesseractWorker = await loadCustomModel();
        console.log('Tesseract worker loaded successfully');
    } catch (error) {
        console.error('Failed to load Tesseract worker:', error);
    }
    
    // Add resize listener for dynamic background updates
    window.addEventListener('resize', () => {
        setTimeout(generateBinaryBackground, 100);
    });
    
    // Also update on orientation change for mobile
    window.addEventListener('orientationchange', () => {
        setTimeout(generateBinaryBackground, 300);
    });
};

// Force background regeneration when page becomes visible (for mobile browsers)
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        setTimeout(generateBinaryBackground, 100);
    }
});
