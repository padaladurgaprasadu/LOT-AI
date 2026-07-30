"""
Real security scanning engine.
Uses regex patterns and Bandit to find OWASP Top 10 vulnerabilities.
"""

import re
import subprocess
import json
import tempfile
import os

SECURITY_PATTERNS = {
    "SQLi": (r"(?i)(SELECT|INSERT|UPDATE|DELETE|DROP).*?\s+FROM\s+.*?\s+WHERE\s+.*?=\s*['\"].*?%s|f['\"].*?\{", "HIGH"),
    "XSS": (r"(?i)<\s*script\s*>.*?</\s*script\s*>|innerHTML\s*=", "HIGH"),
    "Hardcoded Secrets": (r"(?i)(password|secret|token|api_key|apikey)\s*=\s*['\"][a-zA-Z0-9]{10,}['\"]", "CRITICAL"),
    "Eval/Exec": (r"(?i)\b(eval|exec)\s*\(", "CRITICAL"),
    "Path Traversal": (r"(?i)\.\./\.\./|open\s*\(\s*request\.", "HIGH"),
    "Insecure Deserialization": (r"(?i)\b(pickle\.loads|yaml\.load)\s*\(", "CRITICAL"),
    "XXE": (r"(?i)\b(xml\.sax|xml\.etree|lxml)\b", "MEDIUM"),
    "CSRF": (r"(?i)(@csrf_exempt|disable_csrf)", "MEDIUM")
}

def scan_code(code: str, language: str = 'python') -> dict:
    """Scans code for security vulnerabilities."""
    findings = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines):
        for vuln_type, (pattern, severity) in SECURITY_PATTERNS.items():
            if re.search(pattern, line):
                findings.append({
                    "type": vuln_type,
                    "severity": severity,
                    "line": i + 1,
                    "description": f"Potential {vuln_type} detected."
                })

    if language == 'python':
        with tempfile.NamedTemporaryFile(suffix=".py", mode='w', delete=False, encoding='utf-8') as f:
            f.write(code)
            tmp_path = f.name
        
        try:
            result = subprocess.run(["bandit", "-r", tmp_path, "-f", "json", "-q"], stdout=subprocess.PIPE, text=True)
            if result.stdout:
                try:
                    bandit_data = json.loads(result.stdout)
                    for issue in bandit_data.get('results', []):
                        findings.append({
                            "type": issue.get('issue_text', 'Bandit Finding'),
                            "severity": issue.get('issue_severity', 'MEDIUM').upper(),
                            "line": issue.get('line_number', 0),
                            "description": issue.get('more_info', '')
                        })
                except json.JSONDecodeError:
                    pass
        except FileNotFoundError:
            pass # Bandit not installed
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    critical_count = sum(1 for f in findings if f['severity'] == 'CRITICAL')
    high_count = sum(1 for f in findings if f['severity'] == 'HIGH')
    
    overall_risk = "HIGH" if critical_count > 0 or high_count > 1 else "MEDIUM" if findings else "LOW"
    is_safe = len(findings) == 0

    return {
        "findings": findings,
        "overall_risk": overall_risk,
        "is_safe": is_safe
    }

def inject_security_scanner_prompt(system_prompt: str) -> str:
    """Injects security scanning directive into the system prompt."""
    directive = "\n[SECURITY DIRECTIVE]: Never hardcode secrets. Validate all inputs to prevent SQLi and XSS.\n"
    return system_prompt + directive
