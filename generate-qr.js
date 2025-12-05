const QRCode = require('qrcode');
const fs = require('fs');

// Deployed application URL
const websiteUrl = 'https://wfic-util-01.clemson.edu/decoder/';

async function generateQRCode() {
    try {
        // Generate QR code as SVG
        const qrSvg = await QRCode.toString(websiteUrl, {
            type: 'svg',
            width: 300,
            margin: 2,
            color: {
                dark: '#000000ff',  
                light: '#FFFFFF'
            }
        }); 
        
        // Generate QR code as PNG
        await QRCode.toFile('qr-code.png', websiteUrl, {
            width: 300,
            margin: 2,
            color: {
                dark: '#000000ff',
                light: '#FFFFFF'
            }
        });
        
        // Save SVG version
        fs.writeFileSync('qr-code.svg', qrSvg);
        
        console.log('QR codes generated successfully!');
        console.log('Website URL:', websiteUrl);
        console.log('Files created: qr-code.png, qr-code.svg');
        
    } catch (error) {
        console.error('Error generating QR code:', error);
    }
}

generateQRCode();
