import sys
import os
import io

sys.path.insert(0, os.path.abspath('.'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from backend.utils.media_fetcher import fetch_wikimedia_image

terms = ["Tirupati", "Elon Musk", "Taj Mahal", "Paris", "NVIDIA", "London"]

for term in terms:
    res = fetch_wikimedia_image(term)
    print(f"Term: '{term}' => Image URL: {res}")
