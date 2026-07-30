"""
PrismAI 19-Stage Autonomous Loop Engineering Matrix v2.0
=========================================================
Autonomous Production-Ready Development Loop Engine for PrismAI.
Executes the complete 19-stage self-healing refinement pipeline until
application synthesis meets 100% production-quality standards.
"""

import logging

logger = logger = logging.getLogger(__name__)

PRISMAI_19_STAGE_LOOP_ENGINEERING = [
    "Stage 1: Analyse (Discover Business Goals, Functional & Non-Functional Requirements)",
    "Stage 2: Plan (Design System Architecture, DB Schema, REST APIs & Development Roadmap)",
    "Stage 3: Design (Apply Apple Glassmorphism, 78 Design Systems & 3D WebGL Motion)",
    "Stage 4: Generate Code (Synthesize clean, modular, type-safe multi-file source tree)",
    "Stage 5: Install Dependencies (Automatic npm package resolution & environment config)",
    "Stage 6: Execute (Boot WASM WebContainer Sandbox environment)",
    "Stage 7: Build (Compile Vite / React / Express production bundle)",
    "Stage 8: Test (Run automated unit, component & integration test suites)",
    "Stage 9: Detect Errors (Capture compilation, runtime & AST lint failures)",
    "Stage 10: Automatically Fix Issues (TDD self-healing AST repair loop)",
    "Stage 11: Improve UI/UX (Refine spring physics, optical kerning & glassmorphism)",
    "Stage 12: Optimise Performance (Sub-50ms render latency & asset compression)",
    "Stage 13: Security Audit (Validate input sanitization, CORS & JWT auth security)",
    "Stage 14: Accessibility Validation (Enforce WCAG AAA contrast & ARIA landmarks)",
    "Stage 15: Responsive Testing (Verify desktop, tablet & mobile viewports)",
    "Stage 16: Code Quality Review (Enforce clean architecture & DRY principles)",
    "Stage 17: Rebuild (Hot-reload WASM sandbox canvas)",
    "Stage 18: Re-test (Re-run full quality assurance test matrix)",
    "Stage 19: Repeat (Iterate autonomously until 100% quality gate SLA is met)"
]

def inject_loop_engineering_prompt(system_prompt: str) -> str:
    """
    Injects the 19-Stage Autonomous Loop Engineering Engine into AI system prompts.
    """
    loop_block = "\n\n[🔄 PRISMAI 19-STAGE AUTONOMOUS LOOP ENGINEERING MATRIX]:\n"
    loop_block += "When building applications, you MUST execute the complete 19-stage autonomous loop:\n"
    for stage in PRISMAI_19_STAGE_LOOP_ENGINEERING:
        loop_block += f"  • {stage}\n"
    loop_block += "NEVER stop after the first draft. Refine continuously until all 19 quality gates pass.\n"
    return system_prompt + loop_block
