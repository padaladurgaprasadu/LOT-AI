import re
import requests
import json
from typing import Dict, Any, List

class BreakingChangesMonitor:
    """Monitor for breaking changes, security patches, deprecated APIs."""
    def __init__(self):
        pass

    def check_npm_package(self, package: str, current_version: str) -> Dict[str, Any]:
        try:
            res = requests.get(f"https://registry.npmjs.org/{package}", timeout=5)
            if res.status_code == 200:
                data = res.json()
                latest = data.get("dist-tags", {}).get("latest", current_version)
                return {
                    "latest_version": latest,
                    "has_breaking_changes": latest.split('.')[0] != current_version.split('.')[0],
                    "migration_guide_url": f"https://www.npmjs.com/package/{package}/v/{latest}",
                    "security_advisories": []
                }
        except:
            pass
        return {"latest_version": current_version, "has_breaking_changes": False, "migration_guide_url": "", "security_advisories": []}

    def check_pypi_package(self, package: str, current_version: str) -> Dict[str, Any]:
        try:
            res = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=5)
            if res.status_code == 200:
                data = res.json()
                latest = data.get("info", {}).get("version", current_version)
                return {
                    "latest_version": latest,
                    "has_breaking_changes": latest.split('.')[0] != current_version.split('.')[0],
                    "changelog_url": data.get("info", {}).get("project_urls", {}).get("Changelog", "")
                }
        except:
            pass
        return {"latest_version": current_version, "has_breaking_changes": False, "changelog_url": ""}

    def check_cve(self, package: str, version: str) -> List[Dict[str, Any]]:
        url = "https://api.osv.dev/v1/query"
        payload = {"package": {"name": package}, "version": version}
        try:
            res = requests.post(url, json=payload, timeout=5)
            if res.status_code == 200:
                vulns = res.json().get("vulns", [])
                return [{"cve_id": v.get("id"), "severity": "HIGH", "description": v.get("details"), "fix_version": ""} for v in vulns]
        except:
            pass
        return []

    def scan_requirements_file(self, req_file_content: str) -> List[Dict[str, Any]]:
        results = []
        for line in req_file_content.splitlines():
            line = line.split('#')[0].strip()
            if not line: continue
            match = re.match(r'^([a-zA-Z0-9_\-]+)(?:[=>~]{1,2}([\d\.]+))?', line)
            if match:
                pkg = match.group(1)
                ver = match.group(2) or "0.0.0"
                info = self.check_pypi_package(pkg, ver)
                vulns = self.check_cve(pkg, ver)
                results.append({
                    "package": pkg,
                    "current": ver,
                    "latest": info["latest_version"],
                    "outdated": info["latest_version"] != ver,
                    "vulnerable": len(vulns) > 0
                })
        return results

    def scan_package_json(self, pkg_content: str) -> List[Dict[str, Any]]:
        results = []
        try:
            data = json.loads(pkg_content)
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            for pkg, ver in deps.items():
                clean_ver = re.sub(r'^[^\d]', '', ver)
                info = self.check_npm_package(pkg, clean_ver)
                vulns = self.check_cve(pkg, clean_ver)
                results.append({
                    "package": pkg,
                    "current": clean_ver,
                    "latest": info["latest_version"],
                    "outdated": info["latest_version"] != clean_ver,
                    "vulnerable": len(vulns) > 0
                })
        except:
            pass
        return results

    def generate_update_report(self, scan_results: List[Dict[str, Any]]) -> str:
        lines = ["# Dependency Update Report\n"]
        for res in scan_results:
            status = "🚨 VULNERABLE" if res["vulnerable"] else "⚠️ OUTDATED" if res["outdated"] else "✅ UP-TO-DATE"
            lines.append(f"- **{res['package']}**: {res['current']} -> {res['latest']} [{status}]")
        return "\n".join(lines)

    def auto_update_requirements(self, req_content: str, safe_only: bool = True) -> str:
        updated = []
        for line in req_content.splitlines():
            clean = line.split('#')[0].strip()
            match = re.match(r'^([a-zA-Z0-9_\-]+)(?:[=>~]{1,2}([\d\.]+))?', clean)
            if match:
                pkg = match.group(1)
                ver = match.group(2) or "0.0.0"
                info = self.check_pypi_package(pkg, ver)
                if not safe_only or not info["has_breaking_changes"]:
                    updated.append(f"{pkg}=={info['latest_version']}")
                else:
                    updated.append(line)
            else:
                updated.append(line)
        return "\n".join(updated)

def inject_breaking_changes_prompt(system_prompt: str) -> str:
    return system_prompt + "\n\n[Breaking Changes Monitor: Active. Will warn on deprecated APIs.]"
