import urllib.request
import urllib.error
import urllib.parse
import json
import base64
from typing import Dict, List, Any, Optional

class GitHubAgent:
    """GitHub automation agent using REST API via urllib."""
    
    BASE_URL = "https://api.github.com"

    def _request(self, method: str, endpoint: str, data: dict = None, token: str = None) -> Any:
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "LOT AI-GitHubAgent"
        }
        if token:
            headers["Authorization"] = f"token {token}"
            
        req_data = None
        if data is not None:
            req_data = json.dumps(data).encode('utf-8')
            headers["Content-Type"] = "application/json"
            
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                return json.loads(content) if content else {}
        except urllib.error.URLError as e:
            if hasattr(e, 'read'):
                print(e.read().decode('utf-8'))
            return {}

    def create_repo(self, name: str, description: str, private: bool = False, token: str = None) -> Dict[str, Any]:
        data = {"name": name, "description": description, "private": private}
        return self._request("POST", "/user/repos", data, token)

    def create_issue(self, owner: str, repo: str, title: str, body: str, labels: List[str] = None, token: str = None) -> Dict[str, Any]:
        data = {"title": title, "body": body, "labels": labels or []}
        return self._request("POST", f"/repos/{owner}/{repo}/issues", data, token)

    def create_pr(self, owner: str, repo: str, title: str, body: str, head: str, base: str = 'main', token: str = None) -> Dict[str, Any]:
        data = {"title": title, "body": body, "head": head, "base": base}
        return self._request("POST", f"/repos/{owner}/{repo}/pulls", data, token)

    def create_branch(self, owner: str, repo: str, branch_name: str, from_branch: str = 'main', token: str = None) -> bool:
        ref_data = self._request("GET", f"/repos/{owner}/{repo}/git/ref/heads/{from_branch}", token=token)
        if not ref_data or "object" not in ref_data:
            return False
        
        sha = ref_data["object"]["sha"]
        data = {"ref": f"refs/heads/{branch_name}", "sha": sha}
        res = self._request("POST", f"/repos/{owner}/{repo}/git/refs", data, token)
        return "ref" in res

    def commit_files(self, owner: str, repo: str, branch: str, files: Dict[str, str], message: str, token: str = None) -> bool:
        """Simulated multi-file commit for simplicity. In reality requires trees and commits API."""
        return True

    def get_repo_info(self, owner: str, repo: str) -> Dict[str, Any]:
        return self._request("GET", f"/repos/{owner}/{repo}")

    def search_repos(self, query: str, language: str = None, sort: str = 'stars') -> List[Dict[str, Any]]:
        q = query
        if language:
            q += f" language:{language}"
        encoded_q = urllib.parse.quote(q)
        res = self._request("GET", f"/search/repositories?q={encoded_q}&sort={sort}")
        return res.get("items", [])

    def get_repo_contents(self, owner: str, repo: str, path: str = '') -> List[Dict[str, Any]]:
        res = self._request("GET", f"/repos/{owner}/{repo}/contents/{path}")
        if isinstance(res, list):
            return res
        return [res] if res else []

    def trigger_workflow(self, owner: str, repo: str, workflow_id: str, ref: str = 'main', token: str = None) -> bool:
        data = {"ref": ref}
        res = self._request("POST", f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches", data, token)
        return res is not None

    def list_issues(self, owner: str, repo: str, state: str = 'open') -> List[Dict[str, Any]]:
        return self._request("GET", f"/repos/{owner}/{repo}/issues?state={state}")

def inject_github_prompt(system_prompt: str, task: str) -> str:
    return f"{system_prompt}\\n\\nGitHub Task:\\n{task}\\n\\nYou are an expert GitHub automation agent."
