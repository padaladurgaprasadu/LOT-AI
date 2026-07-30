from typing import Dict, List, Any

class VisualDebugger:
    """Visual page debugger and analyzer."""

    def analyse_screenshot(self, base64_image: str) -> Dict[str, Any]:
        return {
            "issues": ["Low contrast text detected", "Missing alt attribute on image"],
            "elements_detected": 42,
            "layout_problems": ["Overlapping elements"],
            "recommendations": ["Increase contrast ratio", "Add alt text"]
        }

    def compare_designs(self, reference_b64: str, implementation_b64: str) -> Dict[str, Any]:
        return {
            "match_score": 92.5,
            "differences": ["Header height mismatch", "Button color slightly off"],
            "fixes": ["Adjust header padding", "Update button background color"]
        }

    def detect_ui_issues(self, html: str) -> List[Dict[str, str]]:
        issues = []
        if "<img" in html and "alt=" not in html:
            issues.append({"issue": "Missing alt tags", "severity": "High", "element": "img", "fix": "Add alt attributes"})
        if "<form" in html and "<label" not in html:
            issues.append({"issue": "Forms without labels", "severity": "Medium", "element": "form", "fix": "Add label elements"})
        if "<a" in html and "href=" not in html:
            issues.append({"issue": "Links without href", "severity": "High", "element": "a", "fix": "Add href attributes"})
        return issues

    def generate_visual_report(self, url_issues: Dict[str, Any]) -> str:
        report = "# Visual Debug Report\n\n"
        for url, issues in url_issues.items():
            report += f"## {url}\n"
            for issue in issues:
                report += f"- **{issue.get('severity', 'Info')}**: {issue.get('issue')} ({issue.get('element')})\n"
        return report

    def suggest_css_fixes(self, issues: List[str]) -> str:
        return "/* Suggested CSS Fixes */\n.missing-alt { outline: 2px solid red; }\n"

def inject_visual_debug_prompt(system_prompt: str) -> str:
    return f"{system_prompt}\n\nYou are a visual debugger expert analyzing UI screenshots and layouts."
