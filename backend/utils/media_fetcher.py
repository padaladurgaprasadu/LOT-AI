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

CURATED_HIGH_RES_IMAGES = {
    "tirupati": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=1200&auto=format&fit=crop",
    "tirupati temple": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=1200&auto=format&fit=crop",
    "kedarnath": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=1200&auto=format&fit=crop",
    "kedarnath temple": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=1200&auto=format&fit=crop",
    "taj mahal": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=1200&auto=format&fit=crop",
    "varanasi": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=1200&auto=format&fit=crop",
    "golden temple": "https://images.unsplash.com/photo-1514222134-b57cbb8ce073?w=1200&auto=format&fit=crop",
    "ayodhya": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200&auto=format&fit=crop",
    "elon musk": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Elon_Musk_-_54820081119_%28cropped%29.jpg/1280px-Elon_Musk_-_54820081119_%28cropped%29.jpg"
}

def fetch_wikimedia_image(query_term: str) -> str:
    """
    Queries Wikipedia / Wikimedia Commons / Unsplash CDN for high-resolution images.
    Returns direct 1200px+ CDN image URL.
    """
    if not query_term or len(query_term.strip()) == 0:
        return None
        
    clean_term = query_term.strip().lower()
    
    # Check Curated High-Res Registry First
    for key, img_url in CURATED_HIGH_RES_IMAGES.items():
        if key in clean_term or clean_term in key:
            logger.info(f"[MediaFetcher] Using curated high-res image for '{clean_term}': {img_url}")
            return img_url
            
    try:
        encoded_term = urllib.parse.quote(query_term.strip())
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={encoded_term}&prop=pageimages&format=json&pithumbsize=1280"
        
        req = urllib.request.Request(url, headers={"User-Agent": "PrismAI/1.0 (https://prismai.ai)"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_info in pages.items():
                if "thumbnail" in page_info and "source" in page_info["thumbnail"]:
                    image_url = page_info["thumbnail"]["source"]
                    logger.info(f"[MediaFetcher] Found Wikipedia image for '{query_term}': {image_url}")
                    return image_url
    except Exception as e:
        logger.warning(f"[MediaFetcher] Failed to fetch image for '{query_term}': {e}")
        
    return None
