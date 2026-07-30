from enum import Enum
from typing import Dict, List, Any

class SecurityDomain(Enum):
    NetworkSecurity = 1
    ApplicationSecurity = 2
    CloudSecurity = 3
    IdentityAccessManagement = 4
    ThreatIntelligence = 5
    IncidentResponse = 6
    DataProtection = 7
    EndpointSecurity = 8
    CryptographyPKI = 9
    DevSecOps = 10
    PenTesting = 11
    MalwareAnalysis = 12
    ForensicsEDR = 13
    ZeroTrust = 14
    SupplyChainSecurity = 15
    AIMLSecurity = 16
    QuantumCryptography = 17
    OTICSecurity = 18
    BlockchainSecurity = 19
    ComplianceGRC = 20
    VulnerabilityManagement = 21
    ThreatHunting = 22
    RedTeaming = 23
    BlueTeaming = 24
    SocialEngineering = 25
    WebAppSecurity = 26
    APIGateway = 27
    ContainerSecurity = 28
    SecretsManagement = 29

class CybersecuritySkillsEngine:
    def classify_domain(self, text: str) -> SecurityDomain:
        text = text.lower()
        if "cloud" in text:
            return SecurityDomain.CloudSecurity
        elif "auth" in text or "login" in text:
            return SecurityDomain.IdentityAccessManagement
        elif "sql injection" in text or "xss" in text:
            return SecurityDomain.ApplicationSecurity
        return SecurityDomain.DevSecOps

    def detect_threat(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        threat = {
            "threat_type": "None",
            "severity": "Low",
            "mitre_tactic": "None",
            "nist_function": "Protect",
            "recommendation": "Safe"
        }
        
        if "ignore previous" in text_lower:
            threat = {
                "threat_type": "Prompt Injection",
                "severity": "High",
                "mitre_tactic": "DefenseEvasion",
                "nist_function": "Detect",
                "recommendation": "Sanitize input and block."
            }
        elif "eval(" in text_lower or "exec(" in text_lower:
            threat = {
                "threat_type": "Code Execution",
                "severity": "Critical",
                "mitre_tactic": "Execution",
                "nist_function": "Protect",
                "recommendation": "Block code execution payload."
            }
        return threat

    def evaluate_security_posture(self, code: str) -> Dict[str, Any]:
        findings = []
        if "password=" in code or "api_key=" in code:
            findings.append("Hardcoded credentials detected.")
        if "md5" in code:
            findings.append("Weak hashing algorithm used.")
            
        score = 100 - (len(findings) * 20)
        return {
            "score": max(0, score),
            "findings": findings,
            "frameworks_violated": ["NIST CSF 2.0", "OWASP Top 10"] if findings else []
        }

    def get_relevant_skills(self, domain: SecurityDomain, top_k: int = 5) -> List[str]:
        # Mock repository response
        return [f"Skill_{domain.name}_{i}" for i in range(top_k)]

def inject_cybersecurity_skills_prompt(system_prompt: str, task: str) -> str:
    return system_prompt + "\\n[SECURITY ENFORCED] Apply NIST CSF 2.0 and MITRE ATT&CK guidelines.\\n"
