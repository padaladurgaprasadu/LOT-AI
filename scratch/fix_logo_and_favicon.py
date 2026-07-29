import os
import sys
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8')

uploaded_png = r"C:\Users\DELL\.gemini\antigravity\brain\12ed7365-83b0-4b77-b090-8e3e9500d7a6\.user_uploaded\media__1785324123465.png"

# 1. Open original HD image
img = Image.open(uploaded_png).convert("RGBA")

# 2. Create High-Contrast Favicon with dark rounded background for browser tabs
fav_size = (128, 128)
favicon = Image.new("RGBA", fav_size, (0, 0, 0, 0))

# Draw dark rounded square background (#121214)
draw = ImageDraw.Draw(favicon)
draw.rounded_rectangle([(0, 0), (127, 127)], radius=24, fill=(18, 18, 24, 255))

# Resize prism graphic to fit inside rounded box with padding
resized_prism = img.resize((104, 104), Image.LANCZOS)
favicon.paste(resized_prism, (12, 12), resized_prism)

# Save Favicon to public folder
pub_dir = r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\public"
fav_png_path = os.path.join(pub_dir, "favicon.png")
fav_ico_path = os.path.join(pub_dir, "favicon.ico")

favicon.save(fav_png_path, "PNG")
favicon.save(fav_ico_path, "ICO", sizes=[(32, 32), (64, 64), (128, 128)])

print(f"✅ High-Contrast Favicon created at: {fav_png_path}")
print(f"✅ Favicon ICO created at: {fav_ico_path}")
