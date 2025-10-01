import os
import glob

def find_font_files():
    """Search for OTF font files in common locations"""
    
    print("=== SEARCHING FOR OTF FONT FILES ===")
    
    # Search locations
    search_paths = [
        ".",  # Current directory
        "..",  # Parent directory
        "../..",  # Grandparent directory
        "C:/Windows/Fonts",  # System fonts
        os.path.expanduser("~/Desktop"),  # Desktop
        os.path.expanduser("~/Downloads"),  # Downloads
    ]
    
    found_fonts = []
    
    for path in search_paths:
        if os.path.exists(path):
            print(f"\nSearching in: {os.path.abspath(path)}")
            try:
                # Search for OTF files
                otf_files = glob.glob(os.path.join(path, "*.otf"))
                otf_files.extend(glob.glob(os.path.join(path, "*.OTF")))
                
                if otf_files:
                    print(f"  Found {len(otf_files)} OTF files:")
                    for font in otf_files:
                        print(f"    - {font}")
                        if "gill" in font.lower() or "sans" in font.lower():
                            found_fonts.append(font)
                else:
                    print("  No OTF files found")
            except Exception as e:
                print(f"  Error searching: {e}")
        else:
            print(f"Path doesn't exist: {path}")
    
    print(f"\n=== GILL SANS CANDIDATES ===")
    if found_fonts:
        print("Found potential Gill Sans fonts:")
        for font in found_fonts:
            print(f"  - {font}")
        
        print(f"\nTo copy a font to training folder, you can:")
        print(f"1. Manually copy the file to: {os.path.abspath('training')}")
        print(f"2. Or tell me which file to copy and I'll create a script")
    else:
        print("No Gill Sans fonts found automatically.")
        print("Please manually locate your Gill Sans OTF files.")
    
    print(f"\n=== MANUAL INSTRUCTIONS ===")
    print(f"1. Find your Gill Sans OTF files")
    print(f"2. Copy them to: {os.path.abspath('training')}")
    print(f"3. Run: python verify_files.py")

if __name__ == "__main__":
    find_font_files()
