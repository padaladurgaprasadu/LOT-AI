"""
PrismAI Sovereign CLI Engine v1.0 — Phase 6
=============================================
Agentic terminal interface that runs the full 37-swarm from any command line.

Commands:
  prismai build "e-commerce platform"  → Full autonomous app synthesis
  prismai review                       → AI code review on current git diff
  prismai debug "error description"    → Root-cause analysis + auto-fix
  prismai architect "system name"      → Full C4 architecture generation
  prismai test                         → Generate + run comprehensive test suite
  prismai secure                       → OWASP security audit + fix recommendations
  prismai optimize                     → Performance profiling + optimisation plan
  prismai ship                         → Production deployment checklist + CI/CD

Phase 4: Browser Intelligence integration (Playwright MCP)
Phase 5: Voice pipeline (already in frontend, backend hooks here)
Phase 7: 3D Visual AI Studio (Three.js architecture renderer directives)
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


# ─────────────────────────── CLI Command Registry ────────────────────────────

CLI_COMMANDS = {
    "build":     ("Autonomous full-stack app synthesis",    "🚀"),
    "review":    ("AI code review on git diff",             "👁️"),
    "debug":     ("Root-cause analysis + auto-fix",        "🔧"),
    "architect": ("C4 architecture generation + ADRs",     "📐"),
    "test":      ("Generate + run comprehensive tests",    "🧪"),
    "secure":    ("OWASP Top 10 audit + fix plan",         "🔒"),
    "optimize":  ("Performance profiling + optimisation",  "⚡"),
    "ship":      ("Production deployment + CI/CD",         "🚢"),
    "research":  ("Web crawl + semantic synthesis",        "🔍"),
    "learn":     ("Teach yourself from documentation",     "📚"),
}

CLI_DIRECTIVE = """
[⌨️ PHASE 6: PRISMAI SOVEREIGN CLI — AGENTIC TERMINAL]:

PrismAI operates as a full Agentic CLI engine. When the user asks about
command-line tasks, scripts, or terminal operations:

1. SYNTHESISE the exact shell command (bash/powershell/zsh as appropriate)
2. VALIDATE the command against security rules (no rm -rf /, no sudo blind runs)
3. EXPLAIN what it does and any risks before executing
4. OFFER to run autonomously via the MCP Filesystem server

Available CLI Command Categories:
  prismai build   → Full-stack autonomous app generation from a description
  prismai review  → AI-powered code review with improvement suggestions
  prismai debug   → Automated root-cause analysis using stack trace + AST analysis
  prismai test    → Generate Playwright E2E + Vitest unit + Pytest test suites
  prismai secure  → OWASP Top 10 automated security audit
  prismai ship    → Full CI/CD pipeline: Docker → K8s manifests → GitHub Actions

AGENTIC COMMAND SYNTHESIS RULES:
  • Never generate destructive commands without explicit confirmation
  • Always add error handling (set -e, try/catch)
  • Always validate inputs before passing to shell
  • Prefer idempotent commands (same result if run multiple times)
  • Add --dry-run flags where available before actual execution
"""

BROWSER_INTELLIGENCE_DIRECTIVE = """
[🌐 PHASE 4: BROWSER INTELLIGENCE ENGINE — PLAYWRIGHT MCP]:

PrismAI has full autonomous browser capabilities via Playwright MCP.
When debugging, testing, or inspecting web applications:

1. LAUNCH: Open real Chromium/Firefox/WebKit browser instance
2. NAVIGATE: Go to the exact URL the user specifies
3. INSPECT: Read DOM, console logs, network requests, screenshots
4. INTERACT: Click buttons, fill forms, submit data
5. SCREENSHOT: Capture visual state for comparison
6. DIAGNOSE: Identify bugs from console errors + network failures

Visual Regression Testing:
  • Capture before/after screenshots on UI changes
  • Pixel-diff comparison to detect visual regressions
  • Lighthouse audit for Core Web Vitals

Live Site Debugging Protocol:
  User: "My checkout page is broken"
  PrismAI:
    1. Opens checkout URL in browser
    2. Screenshots the broken state
    3. Reads console errors
    4. Reads network tab (failed requests)
    5. Identifies root cause
    6. Generates fix + diff

REMEMBER: You have Playwright MCP server active. When relevant, proactively
suggest using browser automation to verify UI behaviour.
"""

THREE_D_STUDIO_DIRECTIVE = """
[🎨 PHASE 7: 3D VISUAL AI STUDIO — THREE.JS ARCHITECTURE CANVAS]:

PrismAI can generate interactive 3D architecture visualisations using Three.js.

When creating architecture diagrams, output in this structured format:
  📐 ARCHITECTURE CANVAS: [System name]
  Nodes: List of system components
  Edges: List of relationships (A→B: "calls/uses/extends")
  Layout: Force-directed / Hierarchical / Circular
  Interactions: Click to drill down, hover for details, orbit camera

3D Visualisation Capabilities:
  • C4 Context Diagram → 3D sphere graph with WebGL shaders
  • Microservices Map → 3D node-link diagram with real-time traffic simulation
  • Data Flow → Animated particle system showing data movement
  • System Health → Live 3D dashboard with Prometheus metrics integration

Design AI Studio:
  When generating UIs, always provide:
  1. Complete glassmorphism design tokens (colours, shadows, blur)
  2. Typography stack (Google Fonts: Inter, Outfit, JetBrains Mono)
  3. Animation specifications (Framer Motion spring configs)
  4. Responsive breakpoints (mobile → tablet → desktop → 4K)
"""

VOICE_AI_DIRECTIVE = """
[🎙️ PHASE 5: VOICE-FIRST AI OS — SUB-200MS PIPELINE]:

PrismAI has a sovereign voice interface. For voice interactions:
  • Understand natural speech commands without exact phrasing
  • Handle domain-specific technical terminology accurately
  • Generate concise, speakable responses (not walls of code)
  • Use speech-friendly formatting: no markdown in voice mode

Voice Command Examples (that PrismAI understands perfectly):
  "Build me a React dashboard with dark mode"
  "What's the best way to scale a PostgreSQL database"
  "Fix the authentication bug in my FastAPI app"
  "Explain microservices architecture to a beginner"
  "Create a Kubernetes deployment for my Node.js service"

Voice Response Format:
  1. Confirm the task in plain English
  2. Give the direct answer/code verbally
  3. Offer to show the full implementation in the UI
"""


def inject_all_remaining_phases(system_prompt: str, task: str = "") -> str:
    """
    Inject Phases 4, 5, 6, 7 directives into system prompt.
    Selectively activates based on task context.
    """
    task_lower = task.lower()

    # Phase 6: CLI (always active for terminal users)
    system_prompt += CLI_DIRECTIVE

    # Phase 4: Browser (activate if URL/web testing mentioned)
    if any(k in task_lower for k in ["browser", "playwright", "url", "website", "debug ui",
                                      "test ui", "screenshot", "click", "form", "broken page"]):
        system_prompt += BROWSER_INTELLIGENCE_DIRECTIVE

    # Phase 7: 3D Studio (activate if architecture/visual mentioned)
    if any(k in task_lower for k in ["architecture", "diagram", "visuali", "3d", "canvas",
                                      "three.js", "system design", "c4", "component"]):
        system_prompt += THREE_D_STUDIO_DIRECTIVE

    # Phase 5: Voice (activate if voice/speak mentioned)
    if any(k in task_lower for k in ["voice", "speak", "audio", "speech", "dictate"]):
        system_prompt += VOICE_AI_DIRECTIVE

    return system_prompt
