import re
from typing import Dict, Any, List

def scan_code(code: str, language: str = 'python') -> Dict[str, Any]:
    findings = []
    lines = code.split('\n')
    
    rules = [
        ('SEC001', 'Critical', 'Potential SQL Injection', r"f\s*['\"].*(SELECT|INSERT|UPDATE|DELETE).*\{.*\}"),
        ('SEC002', 'High', 'Potential XSS', r"\.innerHTML\s*="),
        ('SEC003', 'Critical', 'Hardcoded Secret', r"(password|secret|api_key|token)\s*=\s*['\"][A-Za-z0-9\-_]+['\"]"),
        ('SEC004', 'High', 'Dangerous Eval/Exec', r"(eval|exec)\s*\("),
        ('SEC005', 'High', 'Shell Injection', r"(os\.system|subprocess\.Popen)\s*\("),
        ('SEC006', 'Medium', 'Path Traversal', r"\.\./"),
        ('SEC007', 'Critical', 'Insecure Deserialization', r"pickle\.loads\s*\("),
        ('SEC008', 'Medium', 'Potential SSRF', r"requests\.(get|post)\s*\([^,]+request")
    ]
    
    categories = set()
    
    for i, line in enumerate(lines):
        for rule_id, severity, desc, pattern in rules:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append({
                    'rule_id': rule_id,
                    'severity': severity,
                    'description': desc,
                    'line_number': i + 1,
                    'code_snippet': line.strip()
                })
                categories.add(desc)
                
    risk_score = 100
    for f in findings:
        if f['severity'] == 'Critical': risk_score -= 20
        elif f['severity'] == 'High': risk_score -= 10
        elif f['severity'] == 'Medium': risk_score -= 5
        elif f['severity'] == 'Low': risk_score -= 1
        
    risk_score = max(0, risk_score)
    
    return {
        'findings': findings,
        'risk_score': risk_score,
        'owasp_categories': list(categories)
    }
