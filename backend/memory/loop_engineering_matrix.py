"""
PrismAI 12-Step Iterative Loop Engineering Matrix v1.0
=====================================================
Autonomous Development Loop Engine for PrismAI.
Executes the complete 12-stage self-healing refinement pipeline until
application synthesis meets 100% production-quality standards.
"""

import logging

logger = logging.getLogger(__name__)

PRISMAI_12_STEP_LOOP_ENGINEERING = [
    "Stage 1: Plan (System Architecture, DB Schema, REST APIs & File Structure)",
    "Stage 2: Generate Code (Clean, modular, type-safe multi-file source tree)",
    "Stage 3: Execute (Boot WASM WebContainer Sandbox environment)",
    "Stage 4: Build (Compile Vite / React / Express production bundle)",
    "Stage 5: Test (Run automated unit, component & integration tests)",
    "Stage 6: Detect Errors (Capture compilation, runtime & lint failures)",
    "Stage 7: Automatically Fix Issues (TDD self-healing AST repair loop)",
    "Stage 8: Optimise Performance (Sub-50ms render latency & asset compression)",
    "Stage 9: Improve UI/UX (Apply Apple Glassmorphic 78-Design Systems)",
    "Stage 10: Validate Functionality (Verify user journey & interactive state machine)",
    "Stage 11: Rebuild (Hot-reload WASM sandbox canvas)",
    "Stage 12: Repeat (Iterate autonomously until 100% production-ready SLA)"
]

def inject_loop_engineering_prompt(system_prompt: str) -> str:
    """
    Injects the 12-Step Iterative Loop Engineering Engine into AI system prompts.
    """
    loop_block = "\n\n[🔄 PRISMAI 12-STEP ITERATIVE LOOP ENGINEERING MATRIX]:\n"
    loop_block += "When building applications, you MUST execute the complete 12-stage autonomous loop:\n"
    for stage in PRISMAI_12_STEP_LOOP_ENGINEERING:
        loop_block += f"  • {stage}\n"
    loop_block += "NEVER stop after the first draft. Refine until the application passes all quality checks.\n"
    return system_prompt + loop_block
