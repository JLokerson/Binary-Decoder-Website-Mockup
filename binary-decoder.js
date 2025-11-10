// Generate binary pattern background
function generateBinaryBackground() {
    const fullBinaryString = "01010100 01101000 01101001 01110011 00100000 01110111 01100101 01100010 01110011 01101001 01110100 01100101 00100000 01110111 01100001 01110011 00100000 01101101 01100001 01100100 01100101 00100000 01100010 01111001 00100000 01001010 01110101 01101100 01101001 01100001 00100000 01001100 01101111 01101011 01100101 01110010 01110011 01101111 01101110 ";
    const backgroundDiv = document.getElementById('binaryBackground');
    
    // Use fixed pixel sizes that don't scale with zoom
    const fontSize = 14;
    const lineHeight = 16.8; // Fixed pixel value instead of calculated
    const charWidth = 8.4; // Fixed pixel value instead of calculated
    
    // Use physical viewport dimensions
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    const charsPerLine = Math.floor(viewportWidth / charWidth) + 10;
    const numLines = Math.floor(viewportHeight / lineHeight) + 5;
    
    let fullPattern = '';
    let currentPos = 0;
    
    for (let line = 0; line < numLines; line++) {
        let lineText = '';
        let lineLength = 0;
        
        while (lineLength < charsPerLine) {
            const remainingSpace = charsPerLine - lineLength;
            const availableText = fullBinaryString.slice(currentPos);
            
            if (availableText.length === 0 || currentPos >= fullBinaryString.length) {
                currentPos = 0;
                continue;
            }
            
            if (availableText.length >= remainingSpace) {
                lineText += availableText.slice(0, remainingSpace);
                currentPos += remainingSpace;
                lineLength = charsPerLine;
            } else {
                lineText += availableText;
                lineLength += availableText.length;
                currentPos = 0;
            }
        }
        
        fullPattern += lineText + '\n';
    }
    
    backgroundDiv.textContent = fullPattern;
    
    // Set fixed font size in pixels to prevent zoom scaling
    backgroundDiv.style.fontSize = '14px';
    backgroundDiv.style.lineHeight = '16.8px';
}

// Tesseract worker
let tesseractWorker = null;

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

function binaryToAscii(binaryStr, printableOnly = false) {
    console.log("Input binary string:", binaryStr);
    
    let cleaned = binaryStr
        .replace(/[lI|!]/g, '1')
        .replace(/[OoQD\[\]]/g, '0')
        .replace(/OI/g, '01')
        .replace(/IO/g, '10')
        .replace(/Ol/g, '01')
        .replace(/lO/g, '10')
        .replace(/[^01\s]/g, '')
        .replace(/\s+/g, ' ')
        .trim();
    
    console.log("After OCR corrections:", cleaned);
    
    const words = cleaned.split(/\s+/).filter(word => word.length > 0);
    const validBinaries = words.filter(w => w.length === 8 && /^[01]{8}$/.test(w));
    
    if (validBinaries.length === 0) {
        return '';
    }
    
    let ascii = validBinaries.map(bin => {
        const charCode = parseInt(bin, 2);
        return String.fromCharCode(charCode);
    }).join('');
    
    if (printableOnly) {
        ascii = ascii.split('').filter(c => {
            const code = c.charCodeAt(0);
            return code >= 32 && code <= 126;
        }).join('');
    }
    
    return ascii;
}

function preprocessCanvas(canvas, debugCanvas) {
    const ctx = canvas.getContext('2d');
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    
    for (let i = 0; i < imageData.data.length; i += 4) {
        let avg = (imageData.data[i] + imageData.data[i+1] + imageData.data[i+2]) / 3;
        imageData.data[i] = imageData.data[i+1] = imageData.data[i+2] = avg;
    }
    ctx.putImageData(imageData, 0, 0);
    
    if (debugCanvas) {
        debugCanvas.width = canvas.width;
        debugCanvas.height = canvas.height;
        debugCanvas.getContext('2d').putImageData(imageData, 0, 0);
        document.getElementById('toggleProcessedBtn').style.display = 'inline-block';
    }
}

function runOcrOnCanvas(canvas) {
    document.getElementById('decodedText').textContent = 'Scanning...';
    const scale = 2;
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.width * scale;
    tempCanvas.height = canvas.height * scale;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(canvas, 0, 0, tempCanvas.width, tempCanvas.height);
    
    preprocessCanvas(tempCanvas, document.getElementById('processedCanvas'));
    const imageDataUrl = tempCanvas.toDataURL('image/png');
    
    performOCR(imageDataUrl).then(result => {
        document.getElementById('decodedText').textContent = result;
    });
}

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
    
    if (img.complete && img.naturalWidth > 0) {
        processImage();
    } else {
        img.onload = processImage;
    }
}

// Initialize on page load
window.onload = async () => {
    generateBinaryBackground();
    
    try {
        tesseractWorker = await loadCustomModel();
        console.log('Tesseract worker loaded successfully');
    } catch (error) {
        console.error('Failed to load Tesseract worker:', error);
    }
    
    window.addEventListener('resize', generateBinaryBackground);
};
