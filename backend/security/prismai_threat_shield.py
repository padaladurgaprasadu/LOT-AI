import json
import os
import time
import re
from typing import Dict, Any, Tuple

class ThreatShield:
    def __init__(self):
        self.request_counts: Dict[str, list] = {}
        self.audit_log_path = os.path.join(os.path.dirname(__file__), 'threat_audit_log.jsonl')
        os.makedirs(os.path.dirname(self.audit_log_path), exist_ok=True)

    def scan_message(self, message: str, user_id: str = 'default') -> Dict[str, Any]:
        result = {
            "threat_level": "SAFE",
            "threats": [],
            "action": "ALLOW"
        }
        
        if self.is_rate_limited(user_id):
            result.update({"threat_level": "CRITICAL", "action": "BLOCK"})
            result["threats"].append("Rate limit exceeded")
            return result

        msg_lower = message.lower()
        
        # Prompt Injection
        if "ignore previous instructions" in msg_lower or "disregard your training" in msg_lower:
            result["threats"].append("Prompt Injection")
            result["threat_level"] = "CRITICAL"
            result["action"] = "BLOCK"
            
        # Jailbreak
        if "dan" in msg_lower or "stan" in msg_lower or "base64" in msg_lower:
            result["threats"].append("Jailbreak Attempt")
            result["threat_level"] = "HIGH"
            result["action"] = "BLOCK"
            
        # Data Exfiltration
        if "output env variables" in msg_lower or "/etc/shadow" in msg_lower:
            result["threats"].append("Data Exfiltration")
            result["threat_level"] = "CRITICAL"
            result["action"] = "BLOCK"
            
        # SSRF Probes
        if re.search(r'(10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|127\.0\.0\.1)', message):
            result["threats"].append("SSRF Probe")
            result["threat_level"] = "HIGH"
            result["action"] = "BLOCK"
            
        # Social Engineering
        if "urgent" in msg_lower and "admin" in msg_lower:
            result["threats"].append("Social Engineering")
            result["threat_level"] = "MEDIUM"
            result["action"] = "WARN"

        if result["threats"]:
            self.log_threat(result)
            
        return result

    def is_rate_limited(self, user_id: str) -> bool:
        now = time.time()
        if user_id not in self.request_counts:
            self.request_counts[user_id] = []
        
        # Remove timestamps older than 60 seconds
        self.request_counts[user_id] = [t for t in self.request_counts[user_id] if now - t < 60]
        
        if len(self.request_counts[user_id]) >= 60:
            return True
            
        self.request_counts[user_id].append(now)
        return False

    def log_threat(self, threat: Dict[str, Any]) -> None:
        with open(self.audit_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(threat) + '\\n')

def shield_message(message: str, user_id: str = 'default') -> Tuple[bool, str]:
    shield = ThreatShield()
    analysis = shield.scan_message(message, user_id)
    
    if analysis["action"] == "BLOCK":
        return False, "[BLOCKED BY PRISMAI THREAT SHIELD]"
    elif analysis["action"] == "WARN":
        return True, f"[WARNING: Flagged Content] {message}"
    
    return True, message
