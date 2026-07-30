import urllib.request
import urllib.parse
import urllib.error
import html.parser
import re
import json
import threading
import concurrent.futures
from typing import Dict, List, Any, Optional

class SimpleHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.links.append(attr[1])

    def handle_data(self, data):
        cleaned = data.strip()
        if cleaned:
            self.text.append(cleaned)

class WebScraper:
    """Intelligent web scraper using stdlib."""

    def scrape_url(self, url: str, extract_links: bool = False) -> Dict[str, Any]:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8', errors='ignore')
                parser = SimpleHTMLParser()
                parser.feed(content)
                title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
                title = title_match.group(1) if title_match else ""
                
                return {
                    "title": title,
                    "text": "\\n".join(parser.text),
                    "links": parser.links if extract_links else [],
                    "metadata": {},
                    "status": response.getcode()
                }
        except urllib.error.URLError as e:
            return {"title": "", "text": "", "links": [], "metadata": {}, "status": getattr(e, 'code', 500)}

    def scrape_multiple(self, urls: List[str], max_concurrent: int = 5) -> List[Dict[str, Any]]:
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            future_to_url = {executor.submit(self.scrape_url, url): url for url in urls}
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    results.append(future.result())
                except Exception:
                    pass
        return results

    def extract_structured(self, url: str, selectors: Dict[str, str]) -> Dict[str, Any]:
        extracted = {}
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8', errors='ignore')
                for key, pattern in selectors.items():
                    matches = re.findall(pattern, content)
                    extracted[key] = matches
        except Exception:
            pass
        return extracted

    def search_google(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        results = []
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8', errors='ignore')
                parser = SimpleHTMLParser()
                parser.feed(content)
                for i in range(min(num_results, len(parser.links))):
                    results.append({
                        "title": f"Result {i+1}",
                        "url": parser.links[i],
                        "snippet": "Snippet..."
                    })
        except Exception:
            pass
        return results

    def download_pdf(self, url: str, save_path: str) -> str:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(save_path, 'wb') as f:
                f.write(response.read())
            return save_path
        except Exception:
            return ""

    def extract_code_from_page(self, url: str) -> List[str]:
        codes = []
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8', errors='ignore')
                codes = re.findall(r'<pre><code.*?>(.*?)</code></pre>', content, re.IGNORECASE | re.DOTALL)
        except Exception:
            pass
        return [c.strip() for c in codes]

    def monitor_url(self, url: str, check_interval_s: int = 3600) -> Dict[str, Any]:
        return {"url": url, "changed": False, "last_checked": "timestamp"}

    def github_repo_info(self, owner: str, repo: str) -> Dict[str, Any]:
        url = f"https://api.github.com/repos/{owner}/{repo}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception:
            return {}

def inject_scraper_prompt(system_prompt: str, task: str) -> str:
    return f"{system_prompt}\\n\\nWeb Scraping Task:\\n{task}\\n\\nYou are an intelligent web scraper."
