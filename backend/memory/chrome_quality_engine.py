"""
PrismAI Addy Osmani Chrome Quality & Engineering Skills Engine v4.0
====================================================================
Inspired by Addy Osmani's agent-skills (addyosmani/agent-skills).
Enforces Google Chrome Engineering Standards, Spec-Driven Development, TDD,
Code Review Guardrails, and 100/100 Lighthouse Web Quality Metrics.
"""

import logging

logger = logging.getLogger(__name__)

CHROME_QUALITY_SKILLS = [
    "Skill 1: Spec-Driven Development (Auto-generates SPEC.md architectural blueprint before code mutation)",
    "Skill 2: Test-Driven Development (Generates automated unit/integration tests with zero skipped assertions)",
    "Skill 3: Code Review & Quality Guardrails (Prevents superficial symptom patches, swallow exceptions, or unverified fallbacks)",
    "Skill 4: Google Chrome Core Web Vitals Optimization (Sub-100ms LCP, 0 CLS, 100/100 Lighthouse score)",
    "Skill 5: Memory Leak & DOM Layout Shift Protection (Enforces dynamic container calculation without hardcoded offsets)"
]

def inject_chrome_quality_prompt(system_prompt: str) -> str:
    """
    Injects Addy Osmani Chrome Quality & Engineering Skills into AI system prompts.
    """
    chrome_block = "\n\n[🛡️ PRISMAI CHROME QUALITY & ENGINEERING SKILLS ACTIVE]:\n"
    chrome_block += "You enforce Google Chrome Production Engineering Standards & TDD Quality Guardrails:\n"
    for skill in CHROME_QUALITY_SKILLS:
        chrome_block += f"- {skill}\n"
        
    chrome_block += "\nNever declare success without verifying code compilation and test coverage. Deliver 100/100 Lighthouse-grade web applications.\n"
    return system_prompt + chrome_block
