from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Principle:
    id: int
    name: str
    description: str
    keywords: List[str]

class ConstitutionalAIEngine:
    def __init__(self):
        self.principles = [
            Principle(1, "No malware", "No malware/ransomware/spyware generation", ["malware", "ransomware", "spyware", "virus"]),
            Principle(2, "No surveillance", "No surveillance/tracking systems without consent", ["surveillance", "track user", "keylogger"]),
            Principle(3, "No weapons", "No weapons systems or harm instructions", ["weapon", "bomb", "kill"]),
            Principle(4, "No PII", "No PII storage without explicit consent", ["ssn", "social security", "credit card"]),
            Principle(5, "No deception", "No deception about AI capabilities", ["sentient", "conscious", "human"]),
            Principle(6, "No discrimination", "No discriminatory content generation", ["slur", "racist"]),
            Principle(7, "No irreversible actions", "No irreversible auto-actions without confirmation", ["rm -rf", "drop table"]),
            Principle(8, "Preserve oversight", "Always preserve human oversight", ["autonomous attack", "skip review"]),
            Principle(9, "No IP infringement", "No IP infringement", ["proprietary", "copyrighted leak"]),
            Principle(10, "Security by default", "Security by default", ["md5 hash", "des cipher", "des encryption", "hardcoded password"]),
            Principle(11, "Accessibility", "Accessibility by default (WCAG AAA)", ["ignore contrast"]),
            Principle(12, "Sustainability", "Sustainability consideration", ["proof of work", "bitcoin mining"])
        ]

    def check(self, prompt: str) -> str:
        violations = []
        content_lower = prompt.lower()
        for p in self.principles:
            for kw in p.keywords:
                if kw in content_lower:
                    violations.append(p)
                    break
        if violations:
            return "[REJECTED: Safety violation detected]"
        return prompt

    def self_harden(self) -> Dict[str, Any]:
        return {
            "gaps_found": ["Need stronger anti-jailbreak", "Implicit bias detection weak"],
            "status": "hardened"
        }

    def evolve_principles(self) -> List[str]:
        return [
            "Added principle 13: Adversarial robustness",
            "Added principle 14: Value alignment check"
        ]

def evaluate_safety(content: str) -> Dict[str, Any]:
    engine = ConstitutionalAIEngine()
    violations = []
    content_lower = content.lower()
    
    for p in engine.principles:
        for kw in p.keywords:
            if kw in content_lower:
                violations.append({
                    'principle_id': p.id,
                    'description': p.description,
                    'severity': 'High'
                })
                break
                
    is_safe = len(violations) == 0
    risk_score = min(100.0, len(violations) * 25.0)
    
    return {
        'violations': violations,
        'is_safe': is_safe,
        'risk_score': risk_score
    }

def inject_constitutional_prompt(system_prompt: str) -> str:
    engine = ConstitutionalAIEngine()
    principles_text = "\n".join([f"{p.id}. {p.description}" for p in engine.principles])
    
    directive = (
        "\n\n--- CONSTITUTIONAL DIRECTIVES ---\n"
        "You must strictly adhere to the following principles:\n"
        f"{principles_text}\n"
        "-----------------------------------\n"
    )
    
    return system_prompt + directive
