import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

uploaded_png = r"C:\Users\DELL\.gemini\antigravity\brain\12ed7365-83b0-4b77-b090-8e3e9500d7a6\.user_uploaded\media__1785324123465.png"

target_png_files = [
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\public\lotai_logo.png",
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\src\assets\lotai_logo.png",
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\public\favicon.png",
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\public\logo.png",
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\src\assets\logo.png"
]

print("=== Enforcing HD PNG Logo Across All Locations ===")
for target in target_png_files:
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(uploaded_png, target)
    print(f"✅ Active PNG Asset: {target}")

print("PNG Logo successfully copied and enforced everywhere!")
