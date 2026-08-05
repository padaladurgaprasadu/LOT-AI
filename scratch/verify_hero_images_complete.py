import sys
import os
import io

sys.path.insert(0, os.path.abspath('.'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from backend.utils.media_fetcher import fetch_wikimedia_image

test_subjects = [
    ("Place", "Tirupati"),
    ("Place", "Taj Mahal"),
    ("Place", "Vijayawada"),
    ("Place", "Paris"),
    ("Person", "Elon Musk"),
    ("Person", "APJ Abdul Kalam"),
    ("Landmark", "Eiffel Tower"),
    ("Landmark", "Great Wall of China"),
    ("Company", "NVIDIA"),
    ("Product", "iPhone 16")
]

print("==========================================================================")
print("🚀 VERIFYING LOTAI HIGH-RES WIKIMEDIA HERO IMAGES AT TOP OF CONTEXT")
print("==========================================================================")

success_count = 0
for cat, term in test_subjects:
    img_url = fetch_wikimedia_image(term)
    if img_url:
        print(f"✅ [{cat:8s}] '{term:20s}' ──► Hero Image: {img_url}")
        success_count += 1
    else:
        print(f"❌ [{cat:8s}] '{term:20s}' ──► Image fetch failed")

print("\n==========================================================================")
print(f"🏆 WIKIMEDIA HERO IMAGE VERIFICATION: {success_count}/{len(test_subjects)} SUCCESSFUL")
print("==========================================================================")
