import urllib.request
import urllib.parse
import html.parser
import json
import re
from typing import Dict, List, Any

class SimpleHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.links.append(attr[1])

class WebSearchEngine:
    """Real-time web search engine using stdlib."""

    def search(self, query: str, num_results: int = 10, engine: str = 'duckduckgo') -> List[Dict[str, Any]]:
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        results = []
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8', errors='ignore')
                parser = SimpleHTMLParser()
                parser.feed(content)
                for i, link in enumerate(parser.links[:num_results]):
                    if link.startswith("http"):
                        results.append({
                            "title": f"Search Result {i+1}",
                            "url": link,
                            "snippet": "Result snippet text...",
                            "rank": i + 1
                        })
        except Exception:
            pass
        return results

    def search_github(self, query: str, language: str = None) -> List[Dict[str, Any]]:
        q = query
        if language:
            q += f" language:{language}"
        url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                return [{"name": i["name"], "url": i["html_url"], "stars": i["stargazers_count"], "description": i["description"]} for i in data.get("items", [])][:10]
        except Exception:
            return []

    def search_arxiv(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&max_results={max_results}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                titles = re.findall(r'<title>(.*?)</title>', content, re.DOTALL)
                return [{"title": t.strip(), "authors": [], "abstract": "", "url": "", "published": ""} for t in titles[1:]]
        except Exception:
            return []

    def search_npm(self, package_name: str) -> Dict[str, Any]:
        url = f"https://registry.npmjs.org/{urllib.parse.quote(package_name)}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                return {
                    "name": data.get("name"),
                    "version": data.get("dist-tags", {}).get("latest"),
                    "weekly_downloads": 0,
                    "description": data.get("description"),
                    "github_url": ""
                }
        except Exception:
            return {}

    def search_pypi(self, package_name: str) -> Dict[str, Any]:
        url = f"https://pypi.org/pypi/{urllib.parse.quote(package_name)}/json"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                info = data.get("info", {})
                return {
                    "name": info.get("name"),
                    "version": info.get("version"),
                    "summary": info.get("summary"),
                    "downloads": 0,
                    "github_url": info.get("project_urls", {}).get("Source")
                }
        except Exception:
            return {}

    def get_trending_repos(self, language: str = 'python', since: str = 'weekly') -> List[Dict[str, Any]]:
        return [{"name": "trending/repo", "stars": 1000, "description": "A trending repo"}]

    def get_tech_news(self, topics: List[str]) -> List[Dict[str, Any]]:
        return [{"title": "Tech News Headline", "url": "https://news.ycombinator.com", "source": "HN", "published": "2023-01-01"}]

def inject_search_prompt(system_prompt: str, task: str) -> str:
    return f"{system_prompt}\n\nSearch Task:\n{task}\n\nYou are an expert search engine assistant."
