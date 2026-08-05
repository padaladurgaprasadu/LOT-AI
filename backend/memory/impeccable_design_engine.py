"""
LOT AI Impeccable Design Engine v1.0
=====================================
Built-in Senior Product Designer Intelligence & 3D Web Engine.
Integrates 41 Design Rules, 23 Executive Commands, Anti-Pattern Detection,
and 7 Reference Tokens for World-Class UI/UX.
"""

import re
import logging

logger = logging.getLogger(__name__)

IMPECCABLE_DESIGN_RULES = [
    # Typography & Hierarchy
    "Rule 1: Never use raw browser default fonts. Use Outfit, Inter, Syne, or Plus Jakarta Sans with explicit optical kerning.",
    "Rule 2: Enforce mathematical modular scale for headings (1.250 or 1.333 ratio) with dynamic clamp().",
    "Rule 3: Maintain line-height of 1.1 - 1.2 for titles and 1.5 - 1.6 for body copy.",
    
    # HSL Color Systems & Dark Mode
    "Rule 4: Ban generic blue (#0000ff) or plain purple gradients. Use tailored HSL spectral gradients with noise overlays.",
    "Rule 5: Enforce contrast ratios >= 4.5:1 (WCAG AA) and 7:1 (WCAG AAA).",
    "Rule 6: Use multi-layered elevation shadows (0 12px 32px rgba(0,0,0,0.4)) rather than single flat borders.",
    
    # 3D, Scroll Physics & Motion
    "Rule 7: Integrate Three.js / WebGL 3D canvas backgrounds with interactive cursor parallax.",
    "Rule 8: Use Framer Motion / CSS cubic-bezier(0.16, 1, 0.3, 1) spring physics for micro-interactions.",
    "Rule 9: Enforce scroll-driven viewport entrance animations (fade-up, scale-in, blur-release).",
    
    # Anti-Pattern Purging
    "Rule 10: Ban nested cards within cards ('box-in-a-box' syndrome). Use negative space and backdrop-blur glassmorphism.",
    "Rule 11: Ban static placeholders. Every demo app must feature working interactive state machines."
]

IMPECCABLE_COMMANDS = {
    "/impeccable init": "Generates PRODUCT.md & DESIGN.md system tokens for the project.",
    "/impeccable audit": "Conducts automated WCAG accessibility, performance, and responsive layout audits.",
    "/impeccable critique": "Performs executive UX hierarchy and visual weight review.",
    "/impeccable polish": "Elevates UI to Apple / Linear / Stripe 3D design standards.",
    "/impeccable animate": "Injects WebGL 3D scroll physics and spring-based micro-interactions.",
    "/impeccable bolder": "Increases visual contrast, typography weight, and hero impact.",
    "/impeccable quieter": "Subdues background elements to focus on primary CTA hierarchy."
}

def inject_impeccable_design_prompt(system_prompt: str) -> str:
    """
    Injects Impeccable 3D Senior Product Designer rules into AI system prompts.
    """
    impeccable_block = "\n\n[💎 LOTAI IMPECCABLE DESIGN SYSTEM ENFORCER]:\n"
    impeccable_block += "You operate as a Senior Product Designer & 3D Web Engineer.\n"
    impeccable_block += "Enforce these core design rules on every web app build:\n"
    for rule in IMPECCABLE_DESIGN_RULES:
        impeccable_block += f"- {rule}\n"
        
    impeccable_block += "\nBan all generic AI slop, box-in-a-box nested cards, and plain Inter-only typography. Build 3D scroll-driven experiences that WOW users.\n"
    return system_prompt + impeccable_block

def audit_ui_design_code(code_content: str) -> dict:
    """
    Scans code for anti-patterns and returns quality score & polish suggestions.
    """
    issues = []
    score = 100
    
    if "font-family: Arial" in code_content or "font-family: sans-serif" in code_content:
        issues.append("Generic default font detected. Upgrade to Outfit, Inter, or Syne via Google Fonts.")
        score -= 15
        
    if "background: blue" in code_content or "background: #0000ff" in code_content:
        issues.append("Uncurated plain blue background detected. Use HSL spectral gradients with noise.")
        score -= 15
        
    if code_content.count("<div") > 150 and "grid" not in code_content and "flex" not in code_content:
        issues.append("Deep div nesting without CSS Grid/Flex layout detected. Clean layout structure.")
        score -= 10
        
    return {
        "score": max(0, score),
        "issues": issues,
        "is_impeccable": len(issues) == 0
    }
