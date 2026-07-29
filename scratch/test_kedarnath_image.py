import sys
import os
import io

sys.path.insert(0, os.path.abspath('.'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from backend.utils.media_fetcher import fetch_wikimedia_image

img_url = fetch_wikimedia_image("Kedarnath")
print(f"Kedarnath Hero Image URL: {img_url}")
