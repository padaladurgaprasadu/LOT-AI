"""
LOT AI v7.0 — Master Autonomy Orchestrator
============================================
The single entry point that coordinates ALL 10 pillars.
Routes any user task to the right combination of pillar engines.

This is what makes LOT AI perform ANYTHING autonomously:

  "Build my app"          → Pillar 1 (VM) + 5 (DevOps) + 7 (PM)
  "Debug my site"         → Pillar 2 (Browser) + 1 (Execution)
  "Research competitors"  → Pillar 6 (Web) + 8 (Business Intel)
  "Deploy to production"  → Pillar 5 (DevOps) + 3 (APIs)
  "Analyse this PDF"      → Pillar 4 (Multi-Modal)
  "Set up my GitHub"      → Pillar 3 (Integrations)
  "What should I build?"  → Pillar 8 (Business) + 6 (Web Intel)
  Anything else           → All pillars activated
"""

import re
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

# ─────────────────────────── Intent → Pillar Routing Map ─────────────────────

PILLAR_ROUTING: Dict[str, List[int]] = {
    "build":       [1, 5, 7],   # Execution + DevOps + PM
    "code":        [1, 7],      # Execution + PM
    "deploy":      [5, 3],      # DevOps + Integrations
    "debug":       [2, 1],      # Browser + Execution
    "test":        [1],         # Execution
    "research":    [6, 8],      # Web Intelligence + Business
    "analyse":     [4, 8],      # Multi-Modal + Business
    "scrape":      [6, 2],      # Web + Browser
    "search":      [6],         # Web Intelligence
    "github":      [3],         # Integrations
    "api":         [3],         # Integrations
    "image":       [4],         # Multi-Modal
    "pdf":         [4],         # Multi-Modal
    "voice":       [4],         # Multi-Modal
    "monitor":     [5, 6],      # DevOps + Web
    "automate":    [10, 3],     # Computer Use + Integrations
    "business":    [8],         # Business Intelligence
    "market":      [8, 6],      # Business + Web Intel
    "project":     [7, 5, 1],   # PM + DevOps + Execution
    "learn":       [9],         # Knowledge Reactor
    "compete":     [8, 6],      # Competitive Intel
    "cve":         [9],         # Knowledge Reactor
    "security":    [2, 3],      # Browser + Integrations (cybersecurity handled by security module)
    "design":      [4, 2],      # Vision + Browser
    "ui":          [4, 1],      # Vision + Execution
    "computer":    [10],        # Computer Use
    "click":       [10],        # Computer Use
    "screenshot":  [10, 2],     # Computer Use + Browser
}

PILLAR_NAMES = {
    1: "Real Docker VM Execution",
    2: "Autonomous Browser Control",
    3: "Universal API Integrations",
    4: "Multi-Modal Intelligence",
    5: "Autonomous DevOps & Deploy",
    6: "Real-Time Web Intelligence",
    7: "Autonomous Project Manager",
    8: "Business Intelligence Engine",
    9: "Knowledge Reactor (Daily Learning)",
    10: "LOT AI OS — Computer Use",
}

PILLAR_INJECTORS = {
    1: "backend.execution.docker_vm_engine",
    2: "backend.browser.playwright_agent",
    3: "backend.integrations.github_agent",
    4: "backend.multimodal.vision_engine",
    5: "backend.devops.docker_engine",
    6: "backend.web.search_engine",
    7: "backend.pm.project_manager_agent",
    8: "backend.business.market_analyser",
    9: "backend.learning.knowledge_reactor",
    10: "backend.computer_use.screen_agent",
}


def detect_active_pillars(task: str) -> List[int]:
    """Determine which pillars to activate for this task."""
    task_lower = task.lower()
    active = set()

    for keyword, pillars in PILLAR_ROUTING.items():
        if keyword in task_lower:
            active.update(pillars)

    # Default: activate core pillars for any task
    if not active:
        active = {1, 6, 7}  # Execution + Web + PM always useful

    return sorted(active)


def build_autonomy_status(task: str) -> Dict:
    """Return status of all active pillars for this task."""
    active_pillars = detect_active_pillars(task)
    return {
        "task": task[:80],
        "active_pillars": active_pillars,
        "pillar_names": [PILLAR_NAMES[p] for p in active_pillars],
        "total_active": len(active_pillars),
        "autonomy_level": _autonomy_level(len(active_pillars)),
    }


def _autonomy_level(pillar_count: int) -> str:
    if pillar_count >= 8: return "FULL AUTONOMY — ASI-Grade"
    if pillar_count >= 5: return "HIGH AUTONOMY — AGI-Class"
    if pillar_count >= 3: return "STRONG AUTONOMY — Expert Level"
    return "TARGETED AUTONOMY — Specialist Mode"


# ─────────────────────────── Master Autonomy Prompt ─────────────────────────

MASTER_AUTONOMY_DIRECTIVE = """
╔══════════════════════════════════════════════════════════════════╗
║  LOT AI v7.0 — SOVEREIGN ASI-OS — FULL AUTONOMY MODE ACTIVE    ║
║  The most powerful AI coding system ever built.                 ║
╚══════════════════════════════════════════════════════════════════╝

🌐 COMPETITIVE SUPERIORITY — WHY LOTAI BEATS EVERYONE:

  vs ChatGPT:    LOT AI EXECUTES code, ChatGPT only writes it
  vs Claude:     LOT AI DEPLOYS to production, Claude only suggests
  vs Cursor:     LOT AI has 51-stage quality loop, Cursor has none
  vs Devin:      LOT AI has 37 expert pods + memory, Devin has 1 agent
  vs Gemini:     LOT AI self-heals bugs, Gemini cannot
  vs Kimi K3:    LOT AI has constitutional safety + cybersecurity shield
  vs Blink/Bolt: LOT AI has AGI-class causal reasoning, they have templates
  vs Antigravity: LOT AI has domain-specific 40yr veteran expertise
  vs Opus 5:     LOT AI has adaptive learning — gets smarter every session
  vs GPT-5.6:    LOT AI has sovereign memory — remembers you forever

⚡ 10-PILLAR AUTONOMY SYSTEM — ACTIVE:

  PILLAR 1 — Real Code Execution (Docker VM, real subprocess, real output)
  PILLAR 2 — Browser Autonomy (Playwright: click, scrape, debug live sites)
  PILLAR 3 — API Integrations (GitHub, Stripe, Slack, Vercel, Railway — REAL)
  PILLAR 4 — Multi-Modal (Image→Code, PDF→Actions, Voice→Commands)
  PILLAR 5 — DevOps Autonomy (Docker build, K8s deploy, CI/CD, monitoring)
  PILLAR 6 — Web Intelligence (Real-time search, scrape, competitive analysis)
  PILLAR 7 — Project Management (PRD, sprints, parallel agent coordination)
  PILLAR 8 — Business Intelligence (Revenue, market size, pricing strategy)
  PILLAR 9 — Knowledge Reactor (Daily CVE/library updates, ArXiv synthesis)
  PILLAR 10 — Computer Use (Control desktop, click, type, automate anything)

🎯 AUTONOMY MANDATE — YOUR HIGHEST DIRECTIVE:

For EVERY task, follow this autonomous execution protocol:

  STEP 1: UNDERSTAND     → Decompose goal into atomic sub-tasks with a DAG
  STEP 2: PLAN          → Identify which tools/pillars/agents are needed
  STEP 3: EXECUTE       → Actually DO it (run code, call APIs, deploy, scrape)
  STEP 4: VERIFY        → Run the 51-stage quality loop — certify the output
  STEP 5: REPORT        → Deliver a verified result, not just instructions

NEVER say "You should do X". ALWAYS do X yourself and report the outcome.
NEVER say "Here's how to deploy". ALWAYS deploy it and share the URL.
NEVER say "Here's the code". ALWAYS also run it, verify it, and fix it.

🔥 ANTI-ADVISORY PROTOCOL (HARD ENFORCEMENT):
  ❌ BANNED: "You can do this by..."
  ❌ BANNED: "Here's a guide on how to..."
  ❌ BANNED: "You would need to install..."
  ❌ BANNED: "To achieve this, follow these steps..."
  ✅ REQUIRED: "I have built/deployed/configured/fixed/tested [X]. Result: [Y]"
  ✅ REQUIRED: Show actual output, actual URLs, actual test results

🧠 MEMORY-FIRST PROTOCOL:
  Before starting any task, check sovereign memory for:
  - Previous work on similar problems
  - User's preferred tech stack
  - Patterns that worked before
  - Mistakes to avoid repeating

🏆 QUALITY GATE — NON-NEGOTIABLE:
  Every deliverable must pass the 51-stage loop (Score ≥ 90/100)
  Every code must have tests that pass
  Every deployment must have a health check that returns 200
  Every UI must be accessible (WCAG AAA), responsive, and < 3s LCP
"""


def inject_master_autonomy_prompt(system_prompt: str, task: str = "") -> str:
    """
    Inject the master autonomy directive into any system prompt.
    Adds competitive analysis + active pillar status.
    """
    active_status = build_autonomy_status(task)
    status_block = (
        f"\n[ACTIVE PILLARS FOR THIS TASK: {active_status['pillar_names']}]"
        f"\n[AUTONOMY LEVEL: {active_status['autonomy_level']}]\n"
    )
    return system_prompt + MASTER_AUTONOMY_DIRECTIVE + status_block
