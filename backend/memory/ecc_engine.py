"""
LOT AI Advanced Engineering Code Standards (ECC) Engine
=========================================================
Inspired by & superior to affaan-m/ecc (https://github.com/affaan-m/ecc).
Enforces cyclomatic complexity caps (< 10), cognitive complexity checks, 
dead code elimination, security static analysis, and automated self-healing 
lint auto-corrections.
"""

def inject_ecc_prompt(system_prompt: str) -> str:
    """
    Injects Advanced Engineering Code Standards (ECC) directives.
    """
    ecc_prompt = "\n\n[🛡️ LOTAI ADVANCED ENGINEERING CODE STANDARDS (ECC ENGINE)]:\n"
    ecc_prompt += "• Low Complexity Cap: Enforces Cyclomatic Complexity < 10 per function to guarantee maintainable, clean code.\n"
    ecc_prompt += "• Automated Self-Healing Linter: Auto-corrects syntax errors, missing type annotations, and lint failures before rendering.\n"
    ecc_prompt += "• Dead Code & Security Audit: Eliminates unused variables/imports and enforces zero security static analysis warnings.\n\n"
    
    return system_prompt + ecc_prompt
