import re
import urllib.request
from typing import Optional

class WebPerceptionEngine:
    """
    yAI Pillar 3: Autonomous Web Perception
    Allows the Research Agent to physically fetch live internet data to prevent hallucinations.
    Uses standard library urllib for zero-dependency execution.
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 yAI-Research-Agent'
        }

    def strip_html(self, html_content: str) -> str:
        """Removes DOM bloat and returns raw text content."""
        # Remove scripts and styles
        clean = re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
        clean = re.sub(r'<style.*?>.*?</style>', '', clean, flags=re.IGNORECASE | re.DOTALL)
        # Remove HTML tags
        clean = re.sub(r'<.*?>', ' ', clean)
        # Collapse whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean

    def fetch_url(self, url: str) -> Optional[str]:
        """Synchronous fetch of a URL."""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                html = response.read().decode('utf-8')
                text = self.strip_html(html)
                return text[:5000] # Cap context limit to 5000 chars to save tokens
        except Exception as e:
            print(f"[WebPerceptionEngine] Failed to fetch {url}: {e}")
            return None

    def analyze_task_for_web_searches(self, task_description: str) -> str:
        """
        Extracts URLs from the prompt and fetches them.
        In a full implementation, this would also query a search engine (like DuckDuckGo API)
        for keywords like 'Stripe Next.js Docs'.
        """
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', task_description)
        if not urls:
            return ""
            
        perception_data = "LIVE WEB DATA FETCHED:\n"
        for url in urls[:2]: # Limit to 2 urls to prevent blocking
            print(f"[WebPerceptionEngine] Scraping live documentation: {url}")
            content = self.fetch_url(url)
            if content:
                perception_data += f"\n--- Source: {url} ---\n{content}\n"
                
        return perception_data
