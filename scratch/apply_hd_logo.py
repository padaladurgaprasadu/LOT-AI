import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

uploaded_logo = r"C:\Users\DELL\.gemini\antigravity\brain\12ed7365-83b0-4b77-b090-8e3e9500d7a6\.user_uploaded\media__1785323944312.png"

targets = [
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\public\lotai_logo.png",
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\src\assets\lotai_logo.png",
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\public\favicon.png",
    r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\public\logo.png"
]

print("=== Copying New HD LOT Logo to Frontend Locations ===")
for target in targets:
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(uploaded_logo, target)
    print(f"Copied to: {target}")

print("Done updating HD LOT AI Logo across all assets!")
