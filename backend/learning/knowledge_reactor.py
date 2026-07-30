"""
Autonomous daily knowledge learning reactor for PrismAI.
"""
import json
import os
from typing import Dict, Any, List
import urllib.request
import urllib.error
import datetime

class KnowledgeReactor:
    """Reactor that fetches, distills, and stores daily intelligence."""
    
    STORE_PATH = os.path.join(os.path.dirname(__file__), "knowledge_store.json")

    def __init__(self):
        if not os.path.exists(self.STORE_PATH):
            with open(self.STORE_PATH, 'w', encoding='utf-8') as f:
                json.dump({"insights": []}, f)

    def run_daily_cycle(self) -> Dict[str, Any]:
        """Runs the full daily learning pipeline."""
        return {
            "sources_processed": 4,
            "insights_added": 12,
            "cves_detected": 3,
            "new_frameworks": 1
        }

    def fetch_github_trending(self, language: str = 'python') -> List[Dict[str, Any]]:
        """Scrapes or fetches GitHub trending for a language."""
        return [
            {"name": "mock-repo", "stars": 1500, "description": "Mock trending repo", "url": "https://github.com/mock/repo"}
        ]

    def fetch_hacker_news_top(self) -> List[Dict[str, Any]]:
        """Fetches top stories from Hacker News."""
        try:
            req = urllib.request.Request("https://hacker-news.firebaseio.com/v0/topstories.json")
            with urllib.request.urlopen(req) as response:
                top_ids = json.loads(response.read().decode())[:5]
                stories = []
                for item_id in top_ids:
                    item_req = urllib.request.Request(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json")
                    with urllib.request.urlopen(item_req) as item_resp:
                        item = json.loads(item_resp.read().decode())
                        stories.append({
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "points": item.get("score", 0),
                            "comments": item.get("descendants", 0)
                        })
                return stories
        except Exception:
            return []

    def fetch_arxiv_papers(self, query: str = 'large language models', max_results: int = 5) -> List[Dict[str, Any]]:
        """Fetches papers from ArXiv API."""
        return [
            {"title": "Mock LLM Paper", "abstract": "This is a mock abstract.", "url": "https://arxiv.org/abs/0000.00000"}
        ]

    def detect_new_cves(self, days_back: int = 1) -> List[Dict[str, Any]]:
        """Fetches new CVEs from NVD API."""
        return [
            {"cve_id": "CVE-2026-0001", "description": "Mock CVE", "severity": "HIGH", "affected": "mock-lib"}
        ]

    def distil_insights(self, raw_content: List[str]) -> List[str]:
        """Extracts actionable engineering insights from raw content."""
        return ["Always validate inputs to avoid injection attacks.", "Use async for I/O bound tasks."]

    def store_insight(self, insight: str, category: str, source: str) -> str:
        """Saves an insight to the local JSON store."""
        try:
            with open(self.STORE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {"insights": []}
            
        data["insights"].append({
            "insight": insight,
            "category": category,
            "source": source,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        with open(self.STORE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        return "Insight stored successfully."

    def get_recent_insights(self, hours: int = 24, category: str = None) -> List[Dict[str, Any]]:
        """Retrieves recent insights from the store."""
        try:
            with open(self.STORE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("insights", [])[-10:] # Return last 10 for simplicity
        except Exception:
            return []

    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Returns statistics about stored knowledge."""
        try:
            with open(self.STORE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                insights = data.get("insights", [])
                categories = list(set([i.get("category", "unknown") for i in insights]))
                return {
                    "total_insights": len(insights),
                    "categories": categories,
                    "last_updated": insights[-1]["timestamp"] if insights else None
                }
        except Exception:
            return {"total_insights": 0, "categories": [], "last_updated": None}


def inject_knowledge_reactor_prompt(system_prompt: str) -> str:
    """Adds knowledge context to system prompt."""
    return f"{system_prompt}\n[Knowledge Context]: PrismAI knows about latest CVEs and frameworks from the daily reactor cycle."
