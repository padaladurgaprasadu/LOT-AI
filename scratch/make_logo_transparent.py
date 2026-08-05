import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

uploaded_png = r"C:\Users\DELL\.gemini\antigravity\brain\12ed7365-83b0-4b77-b090-8e3e9500d7a6\.user_uploaded\media__1785324123465.png"

img = Image.open(uploaded_png).convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    # Change all near-black pixels to transparent
    # item is (R, G, B, A)
    if item[0] < 35 and item[1] < 35 and item[2] < 35:
        newData.append((0, 0, 0, 0))
    else:
        newData.append(item)

img.putdata(newData)

target_png_files = [
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\public\lotai_logo.png",
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\src\assets\lotai_logo.png",
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\public\favicon.png",
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\public\logo.png",
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\src\assets\logo.png"
]

print("=== Removing Black Background from Logo (Making Transparent PNG) ===")
for target in target_png_files:
    os.makedirs(os.path.dirname(target), exist_ok=True)
    img.save(target, "PNG")
    print(f"✅ Transparent PNG Saved: {target}")

print("Done making logo background 100% transparent!")
