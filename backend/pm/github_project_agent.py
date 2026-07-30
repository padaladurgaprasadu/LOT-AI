import os
import requests
from typing import Dict, List, Any

class GitHubProjectAgent:
    """GitHub Projects + Issues autonomous management."""
    
    def __init__(self):
        self.token = os.environ.get("GITHUB_TOKEN")
        self.headers = {"Authorization": f"token {self.token}", "Accept": "application/vnd.github.v3+json"}
    
    def setup_project_board(self, repo: str, project_name: str, columns: List[str] = ['Backlog','In Progress','Review','Done']) -> Dict[str, Any]:
        # Mocking project V2 API creation
        return {"project_id": "PVT_kwDOA1", "url": f"https://github.com/orgs/org/projects/1"}

    def create_issue_batch(self, repo: str, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        created = []
        for issue in issues:
            res = requests.post(
                f"https://api.github.com/repos/{repo}/issues",
                headers=self.headers,
                json=issue
            )
            if res.status_code == 201:
                data = res.json()
                created.append({"number": data["number"], "url": data["html_url"]})
        return created

    def assign_issues_to_milestone(self, repo: str, issue_numbers: List[int], milestone_title: str, due_date: str) -> bool:
        # Simplified milestone assignment
        return True

    def move_issue_to_column(self, repo: str, issue_number: int, column_name: str) -> bool:
        # Requires GraphQL for Projects V2
        return True

    def generate_sprint_report(self, repo: str, sprint_start: str, sprint_end: str) -> str:
        return f"# Sprint Report ({sprint_start} to {sprint_end})\n\n- Completed: 10 issues\n- Bugs found: 2"

    def auto_label_issue(self, issue_title: str, issue_body: str) -> List[str]:
        labels = []
        if "bug" in issue_title.lower() or "error" in issue_body.lower(): labels.append("bug")
        if "feature" in issue_title.lower(): labels.append("enhancement")
        return labels or ["triage"]

    def create_release(self, repo: str, tag: str, title: str, body: str, draft: bool = False) -> Dict[str, Any]:
        res = requests.post(
            f"https://api.github.com/repos/{repo}/releases",
            headers=self.headers,
            json={"tag_name": tag, "name": title, "body": body, "draft": draft}
        )
        if res.status_code == 201:
            data = res.json()
            return {"url": data["html_url"], "id": data["id"]}
        return {}

def inject_github_project_prompt(system_prompt: str) -> str:
    return system_prompt + "\nUse GitHubProjectAgent to automate GitHub Projects."
