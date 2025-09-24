/**
 * Binary OCR Training Integration
 * This file contains the training results and optimizations from our Tesseract training
 */

class BinaryOCRTraining {
    constructor() {
        // Training results from our Python OCR tool
        this.trainingConfig = {
            // Best configuration found during training - optimized for binary patterns
            tesseract: {
                tessedit_char_whitelist: '01 ',
                tessedit_pageseg_mode: '6',  // Uniform block of text
                preserve_interword_spaces: '1',
                tessedit_ocr_engine_mode: '1', // Neural nets LSTM engine only
                tessedit_write_images: '0',
                user_defined_dpi: '300',
                textord_min_linesize: '2.5'
            },
            // Image preprocessing settings - more aggressive
            preprocessing: {
                scaleFactor: 3,  // Increased scale
                contrastMultiplier: 2.0,  // Higher contrast
                whiteThreshold: 140,
                blackThreshold: 100
            }
        };
        
        // Common OCR errors and corrections based on training
        this.errorCorrections = {
            // Common misrecognitions from training data
            'l': '1', 'I': '1', 'i': '1', '|': '1',
            'O': '0', 'o': '0', 'Q': '0', 'D': '0'
        };
        
        // Performance metrics from training
        this.metrics = {
            confidence: 100.0,
            accuracy: 0.95, // Based on our training results
            supportedPatterns: ['8-bit binary groups separated by spaces']
        };
    }
    
    /**
     * Apply error corrections based on training data
     */
    correctOCRErrors(text) {
        let corrected = text;
        
        // Apply character-level corrections
        for (const [wrong, correct] of Object.entries(this.errorCorrections)) {
            corrected = corrected.replace(new RegExp(wrong, 'g'), correct);  
        }
        
        // Additional pattern-based corrections
        corrected = this.fixCommonPatterns(corrected);
        
        // Extract binary patterns more aggressively
        corrected = this.extractBinaryPatterns(corrected);
        
        return corrected;
    }

    /**
     * Extract binary patterns from noisy OCR text
     */
    extractBinaryPatterns(text) {
        console.log("Extracting binary patterns from:", text.substring(0, 200) + "...");
        
        // Find all sequences that look like binary patterns
        const binaryLikePatterns = [];
        
        // First, try to extract continuous binary sequences from the entire text
        const allBinaryDigits = text.replace(/[^01]/g, '');
        console.log("All binary digits found:", allBinaryDigits);
        
        if (allBinaryDigits.length >= 8) {
            // Split into 8-character groups
            const groups = allBinaryDigits.match(/.{1,8}/g) || [];
            for (const group of groups) {
                if (group.length === 8) {
                    binaryLikePatterns.push(group);
                } else if (group.length >= 6) {
                    // Pad shorter groups at the end
                    binaryLikePatterns.push(group.padEnd(8, '0'));
                }
            }
        }
        
        // If we didn't get enough patterns, try word-by-word extraction
        if (binaryLikePatterns.length === 0) {
            const words = text.split(/\s+/);
            
            for (const word of words) {
                if (word.length === 0) continue;
                
                // Extract binary digits from each word
                const binaryDigits = word.replace(/[^01]/g, '');
                
                // If we have at least 4 binary digits, consider it a potential pattern
                if (binaryDigits.length >= 4) {
                    // Split into 8-character chunks
                    const chunks = binaryDigits.match(/.{1,8}/g) || [];
                    for (const chunk of chunks) {
                        if (chunk.length >= 6) { // At least 6 digits to be considered valid
                            // Pad to 8 digits if needed (assume missing digits are 0)
                            const padded = chunk.padEnd(8, '0');
                            binaryLikePatterns.push(padded);
                        }
                    }
                }
            }
        }
        
        console.log("Extracted binary patterns:", binaryLikePatterns);
        return binaryLikePatterns.join(' ');
    }    /**
     * Fix common pattern errors found during training
     */
    fixCommonPatterns(text) {
        let fixed = text;
        
        // Fix incomplete binary groups (common OCR issue)
        // If we have 7 consecutive binary digits followed by space, likely missing one digit
        fixed = fixed.replace(/([01]{7})\s/g, (match, group) => {
            console.log(`Warning: Found 7-digit group '${group}', might be missing a digit`);
            return match; // Keep as-is, but log the issue
        });
        
        // Fix groups that are too long (split at 8-character boundaries)
        fixed = fixed.replace(/([01]{9,})/g, (match) => {
            console.log(`Splitting long binary group: ${match}`);
            return match.match(/.{1,8}/g).join(' ');
        });
        
        // Normalize multiple spaces to single spaces
        fixed = fixed.replace(/\s+/g, ' ').trim();
        
        return fixed;
    }
    
    /**
     * Validate binary string format based on training patterns
     */
    validateBinaryString(binaryStr) {
        const validation = {
            isValid: true,
            errors: [],
            warnings: [],
            stats: {}
        };
        
        const words = binaryStr.split(' ').filter(w => w.length > 0);
        
        // Count different word lengths
        const lengthCounts = {};
        words.forEach(word => {
            lengthCounts[word.length] = (lengthCounts[word.length] || 0) + 1;
        });
        
        validation.stats.totalWords = words.length;
        validation.stats.lengthDistribution = lengthCounts;
        
        // Check for 8-bit groups (our training target)
        const validEightBit = words.filter(w => /^[01]{8}$/.test(w));
        validation.stats.valid8BitGroups = validEightBit.length;
        
        // Validation rules based on training
        if (validEightBit.length === 0) {
            validation.isValid = false;
            validation.errors.push('No valid 8-bit binary groups found');
        }
        
        if (words.length > validEightBit.length) {
            const invalid = words.length - validEightBit.length;
            validation.warnings.push(`${invalid} invalid/incomplete binary groups detected`);
        }
        
        // Check for common OCR artifacts
        const hasInvalidChars = /[^01\s]/.test(binaryStr);
        if (hasInvalidChars) {
            validation.warnings.push('Non-binary characters detected (may be OCR errors)');
        }
        
        return validation;
    }
    
    /**
     * Get recommended Tesseract.js options based on training
     */
    getTesseractOptions() {
        return {
            logger: m => { 
                if (m.status === 'recognizing text') {
                    console.log(`OCR Progress: ${Math.round(m.progress * 100)}%`);
                }
            },
            config: this.trainingConfig.tesseract
        };
    }
    
    /**
     * Process image with training-optimized preprocessing
     */
    preprocessImageForOCR(canvas, debugCanvas = null) {
        const ctx = canvas.getContext('2d');
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        
        const config = this.trainingConfig.preprocessing;
        
        // Apply training-optimized preprocessing with more aggressive filtering
        for (let i = 0; i < data.length; i += 4) {
            // Luminance-based grayscale
            const gray = 0.299 * data[i] + 0.587 * data[i+1] + 0.114 * data[i+2];
            
            // More aggressive contrast enhancement for binary images
            let enhanced = ((gray - 128) * (config.contrastMultiplier * 1.5)) + 128;
            
            // Stricter binary threshold - force to pure black/white
            if (enhanced > 128) {
                enhanced = 255; // Pure white
            } else {
                enhanced = 0;   // Pure black
            }
            
            enhanced = Math.max(0, Math.min(255, enhanced));
            data[i] = data[i+1] = data[i+2] = enhanced;
        }
        
        ctx.putImageData(imageData, 0, 0);
        
        // Apply morphological operations to clean up noise
        this.applyMorphology(ctx, canvas.width, canvas.height);
        
        // Copy to debug canvas if provided
        if (debugCanvas) {
            debugCanvas.width = canvas.width;
            debugCanvas.height = canvas.height;
            debugCanvas.getContext('2d').putImageData(ctx.getImageData(0, 0, canvas.width, canvas.height), 0, 0);
        }
        
        return canvas;
    }

    /**
     * Apply morphological operations to clean up binary image
     */
    applyMorphology(ctx, width, height) {
        const imageData = ctx.getImageData(0, 0, width, height);
        const data = imageData.data;
        const newData = new Uint8ClampedArray(data);
        
        // Simple erosion to remove noise
        for (let y = 1; y < height - 1; y++) {
            for (let x = 1; x < width - 1; x++) {
                const idx = (y * width + x) * 4;
                
                // If this pixel is white, check neighbors
                if (data[idx] === 255) {
                    let whiteNeighbors = 0;
                    
                    // Check 3x3 neighborhood
                    for (let dy = -1; dy <= 1; dy++) {
                        for (let dx = -1; dx <= 1; dx++) {
                            const nIdx = ((y + dy) * width + (x + dx)) * 4;
                            if (data[nIdx] === 255) whiteNeighbors++;
                        }
                    }
                    
                    // If less than 5 white neighbors, make this pixel black (remove noise)
                    if (whiteNeighbors < 5) {
                        newData[idx] = newData[idx + 1] = newData[idx + 2] = 0;
                    }
                }
            }
        }
        
        ctx.putImageData(new ImageData(newData, width, height), 0, 0);
    }
    
    /**
     * Complete OCR pipeline with training optimizations
     */
    async recognizeBinaryPattern(imageSource, options = {}) {
        const startTime = Date.now();
        
        try {
            // Get optimized Tesseract options
            const tesseractOptions = this.getTesseractOptions();
            
            console.log("Starting OCR with training config:", tesseractOptions.config);
            
            // Run OCR
            const result = await Tesseract.recognize(imageSource, 'eng', tesseractOptions);
            
            console.log("Raw OCR confidence:", result.data.confidence);
            console.log("Raw OCR text (first 500 chars):", result.data.text.substring(0, 500));
            
            // Apply training-based corrections
            const correctedText = this.correctOCRErrors(result.data.text);
            
            console.log("Corrected text:", correctedText);
            
            // Validate the result
            const validation = this.validateBinaryString(correctedText);
            
            const processingTime = Date.now() - startTime;
            
            return {
                success: true,
                rawText: result.data.text,
                correctedText: correctedText,
                validation: validation,
                confidence: result.data.confidence,
                processingTime: processingTime,
                stats: {
                    charactersRecognized: result.data.text.length,
                    validBinaryGroups: validation.stats.valid8BitGroups,
                    totalWords: validation.stats.totalWords
                }
            };
            
        } catch (error) {
            console.error("OCR pipeline error:", error);
            return {
                success: false,
                error: error.message,
                processingTime: Date.now() - startTime
            };
        }
    }
}

// Export for use in the main application
if (typeof window !== 'undefined') {
    window.BinaryOCRTraining = BinaryOCRTraining;
}