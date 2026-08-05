import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

transparent_png = r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\src\assets\lotai_logo.png"

favicon_target = r"c:\Users\DELL\OneDrive\Desktop\Tatvamasi\yAI\frontend\public\favicon.png"

shutil.copyfile(transparent_png, favicon_target)

print(f"✅ Pure Transparent PNG Favicon copied to: {favicon_target}")
