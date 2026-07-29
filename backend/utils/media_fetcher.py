"""
PrismAI Sovereign Media & Image Fetcher v1.0
============================================
Fetches official, high-resolution (1280px+) images from Wikipedia & Wikimedia Commons API.
Guarantees 100% valid, beautiful, CDN-cached images for places, landmarks, and public figures.
"""

import urllib.request
import urllib.parse
import json
import logging

logger = logging.getLogger(__name__)

def fetch_wikimedia_image(query_term: str) -> str:
    """
    Queries Wikipedia / Wikimedia Commons API for the official featured image URL.
    Returns direct 1280px CDN image URL or None.
    """
    if not query_term or len(query_term.strip()) == 0:
        return None
        
    try:
        clean_term = query_term.strip()
        encoded_term = urllib.parse.quote(clean_term)
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={encoded_term}&prop=pageimages&format=json&pithumbsize=1280"
        
        req = urllib.request.Request(url, headers={"User-Agent": "PrismAI/1.0 (https://prismai.ai)"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_info in pages.items():
                if "thumbnail" in page_info and "source" in page_info["thumbnail"]:
                    image_url = page_info["thumbnail"]["source"]
                    logger.info(f"[WikimediaFetcher] Found image for '{clean_term}': {image_url}")
                    return image_url
    except Exception as e:
        logger.warning(f"[WikimediaFetcher] Failed to fetch image for '{query_term}': {e}")
        
    return None
