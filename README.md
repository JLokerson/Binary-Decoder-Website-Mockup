# Binary Decoder Website

This website takes a photo, image file, or live video feed and translates any binary text into ASCII.

## 🚀 Live Demo

**Website URL:** [https://julia.github.io/Binary-Decoder-Website-Mockup/](https://julia.github.io/Binary-Decoder-Website-Mockup/)

**QR Code for Mobile Access:**
![QR Code](qr-code.png)

## 📱 Quick Access

Scan the QR code above with your mobile device to instantly access the Binary Decoder website!

## 🛠️ Dependencies for Running Locally

To run this project locally, install:

- [Node.js](https://nodejs.org/) (v16 or higher recommended)
- [npm](https://www.npmjs.com/) (comes with Node.js)

## 🏃‍♀️ Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/julia/Binary-Decoder-Website-Mockup.git
   cd Binary-Decoder-Website-Mockup
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start local development server:
   ```bash
   npm start
   ```

4. Open your browser to `http://localhost:3000`

## 🚀 Deployment Instructions

### Method 1: GitHub Pages (Recommended - Free)

#### Step 1: Create GitHub Repository
1. Go to [github.com](https://github.com) and sign in
2. Click the "+" icon in top right → "New repository"
3. Name it `Binary-Decoder-Website-Mockup` (or any name you prefer)
4. Make sure it's **Public** (required for free GitHub Pages)
5. Click "Create repository"

#### Step 2: Upload Your Code to GitHub
**Option A - Using Git Command Line:**
```bash
# Initialize git in your project folder
git init

# Add GitHub repository as remote (replace 'yourusername' with your GitHub username)
git remote add origin https://github.com/yourusername/Binary-Decoder-Website-Mockup.git

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Binary Decoder Website"

# Push to GitHub
git push -u origin main
```

**Option B - Using GitHub Desktop:**
1. Download [GitHub Desktop](https://desktop.github.com/)
2. Click "Add an Existing Repository from your Hard Drive"
3. Select your project folder
4. Click "Publish repository" and choose your GitHub account

**Option C - Upload Files Directly:**
1. On your empty GitHub repository page, click "uploading an existing file"
2. Drag and drop all your project files
3. Click "Commit changes"

#### Step 3: Enable GitHub Pages
1. **Go to your repository** on GitHub.com
2. **Click the "Settings" tab** (at the top of the repository page)
3. **Scroll down** to find the "Pages" section in the left sidebar
4. **In the Pages section:**
   - Under "Source", select "Deploy from a branch"
   - Under "Branch", select "main" (or "master" if that's your default)
   - Under "Folder", select "/ (root)"
   - Click "Save"

#### Step 4: Wait for Deployment
- GitHub will show a message: "Your site is ready to be published at https://yourusername.github.io/Binary-Decoder-Website-Mockup/"
- It may take 5-10 minutes for your site to go live
- You'll get a green checkmark when it's ready

#### Step 5: Test Your Live Website
- Visit: `https://yourusername.github.io/Binary-Decoder-Website-Mockup/`
- Share this URL or generate a QR code for it!

#### Common GitHub Pages Issues:
- **404 Error:** Make sure `index.html` is in the root folder
- **Site not updating:** Changes can take 5-10 minutes to appear
- **Can't find Pages setting:** Repository must be public
- **Build failed:** Check that all file names are correct and no special characters

### Method 2: Manual Deployment with gh-pages

```bash
npm run deploy
```

### Method 3: Other Hosting Platforms

**Netlify:**
1. Drag and drop the project folder to [netlify.com/drop](https://app.netlify.com/drop)
2. Your site will be live instantly with a custom URL

**Vercel:**
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel --prod`
3. Follow the prompts

## 📱 Generate QR Code

To create a QR code for your deployed website:

```bash
npm run generate-qr
```

This creates:
- `qr-code.png` - PNG image
- `qr-code.svg` - SVG vector image

**Note:** Update the URL in `generate-qr.js` with your actual deployment URL before running.

## 🔧 Project Structure

```
Binary-Decoder-Website-Mockup/
├── index.html              # Main landing page
├── take-photo.html         # Camera capture page
├── insert-photo.html       # File upload page
├── scan-camera.html        # Live camera scanning
├── text-input.html         # Manual text input
├── style.css              # Main stylesheet
├── binary-decoder.js      # Core functionality
├── package.json           # Project configuration
├── generate-qr.js         # QR code generator
├── qr-code.png           # Generated QR code (PNG)
├── qr-code.svg           # Generated QR code (SVG)
└── .github/
    └── workflows/
        └── deploy.yml     # Auto-deployment workflow
```

## 📝 Notes

- Camera access requires HTTPS in production (GitHub Pages provides this automatically)
- The website is fully responsive and works on mobile devices
- OCR functionality uses Tesseract.js for client-side text recognition
- All processing happens in the browser - no server required

## 🐛 Troubleshooting

- **Camera not working:** Ensure you're accessing via HTTPS and have granted camera permissions
- **Deployment fails:** Check that your repository is public and GitHub Pages is enabled
- **QR code generation fails:** Make sure you've run `npm install` and updated the URL in `generate-qr.js`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request
