"""
LOT AI Bloom's Taxonomy Router v1.0
=====================================
Routes LOT AI responses through Bloom's Taxonomy 6-level cognitive hierarchy
to match the exact cognitive depth required by the user's current expertise level.

Bloom's Taxonomy Levels:
  Level 1 — Remember:   Define, list, name, recall, recognise, repeat, state
  Level 2 — Understand: Classify, describe, explain, identify, paraphrase, summarise
  Level 3 — Apply:      Demonstrate, execute, implement, solve, use, produce
  Level 4 — Analyse:    Compare, differentiate, examine, experiment, question, test
  Level 5 — Evaluate:   Appraise, argue, critique, defend, judge, justify, prioritise
  Level 6 — Create:     Build, design, develop, formulate, invent, plan, produce

Every prompt type maps to a Bloom's level. LOT AI adjusts:
  • Vocabulary complexity (simple ↔ technical)
  • Explanation depth (concept ↔ edge-cases)
  • Code complexity (minimal ↔ production-grade)
  • Diagram density (none ↔ full C4 architecture)
  • Examples count (many → few as expertise rises)
  • Anti-patterns and tradeoffs (hidden → explicit)
"""

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

# ─────────────────────────── Bloom's Level Definitions ─────────────────────

BLOOM_LEVEL_META = {
    1: {
        "name": "Remember",
        "verbs": ["define", "list", "name", "recall", "recognise", "repeat", "state", "what is"],
        "response_style": "Clear, simple definitions with real-world analogies. Avoid jargon. Use short sentences.",
        "code_complexity": "minimal",        # 5–15 lines, no edge cases
        "explanation_depth": "surface",      # What it is, not how or why
        "examples_count": "many",            # 3–5 examples
        "include_tradeoffs": False,
        "include_antipatterns": False,
        "diagram_type": "simple",            # Basic text/ASCII diagram
        "vocabulary": "plain",               # No technical acronyms
    },
    2: {
        "name": "Understand",
        "verbs": ["explain", "describe", "summarise", "how does", "what does", "why does"],
        "response_style": "Clear explanations with why/how context. Simple examples. Relatable analogies.",
        "code_complexity": "simple",         # 10–30 lines, basic patterns
        "explanation_depth": "conceptual",   # What + How
        "examples_count": "several",         # 2–3 examples
        "include_tradeoffs": False,
        "include_antipatterns": False,
        "diagram_type": "flow",              # Flow diagrams OK
        "vocabulary": "semi-technical",
    },
    3: {
        "name": "Apply",
        "verbs": ["build", "implement", "create", "write code", "make", "develop", "solve", "use"],
        "response_style": "Working code examples with clear structure. Step-by-step implementation guidance.",
        "code_complexity": "standard",       # 30–100 lines, production patterns
        "explanation_depth": "practical",    # What + How + Step-by-step
        "examples_count": "focused",         # 1–2 complete examples
        "include_tradeoffs": True,
        "include_antipatterns": False,
        "diagram_type": "component",         # Component diagrams
        "vocabulary": "technical",
    },
    4: {
        "name": "Analyse",
        "verbs": ["compare", "contrast", "differentiate", "why not", "tradeoffs", "which is better", "examine"],
        "response_style": "Deep technical analysis. Multiple approaches compared. Tradeoffs explicitly surfaced.",
        "code_complexity": "advanced",       # 100+ lines, multiple patterns
        "explanation_depth": "analytical",   # What + How + Why + Tradeoffs
        "examples_count": "comparative",     # Side-by-side comparisons
        "include_tradeoffs": True,
        "include_antipatterns": True,
        "diagram_type": "architecture",      # Full architecture diagrams
        "vocabulary": "expert",
    },
    5: {
        "name": "Evaluate",
        "verbs": ["critique", "review", "assess", "is this good", "optimise", "is this the best", "justify"],
        "response_style": "Critical evaluation with evidence-based judgments. Cite engineering principles.",
        "code_complexity": "expert",         # Production-grade with tests
        "explanation_depth": "evaluative",   # Full critique with evidence
        "examples_count": "targeted",        # 1 definitive best-practice example
        "include_tradeoffs": True,
        "include_antipatterns": True,
        "diagram_type": "full_c4",           # Full C4 model diagrams
        "vocabulary": "principal_engineer",
    },
    6: {
        "name": "Create",
        "verbs": ["design", "architect", "invent", "build system", "from scratch", "end-to-end", "full platform"],
        "response_style": "Autonomous synthesis. Full system design. Novel solutions. Production-ready delivery.",
        "code_complexity": "agi_grade",      # Full multi-file production system
        "explanation_depth": "creation",     # Full PRD + ADRs + Architecture + Code
        "examples_count": "comprehensive",   # Complete working system
        "include_tradeoffs": True,
        "include_antipatterns": True,
        "diagram_type": "interactive_3d",    # 3D interactive architecture canvas
        "vocabulary": "visionary_cto",
    },
}

# Prompt injection templates per Bloom's level
BLOOM_PROMPT_TEMPLATES = {
    1: """
[ADAPTIVE LEVEL: 🟢 Beginner — Bloom's Level 1: REMEMBER]
Respond as a patient senior mentor teaching a complete beginner.
• Use plain English, no jargon, no abbreviations without explanation.
• Start with a one-sentence definition.
• Use real-world analogies (not engineering analogies).
• Include 3–5 concrete examples, moving from simplest to slightly harder.
• Code: Maximum 15 lines. Explain every single line with a comment.
• End with: "Here's what you learned today:" followed by 3 bullet points.
• NEVER say "as you know" or "obviously". The user is learning from zero.
""",
    2: """
[ADAPTIVE LEVEL: 🔵 Learner — Bloom's Level 2: UNDERSTAND]
Respond as a clear-thinking senior engineer explaining to a junior developer.
• Explain the WHAT and the HOW. Not the full WHY yet.
• Use 1–2 relatable analogies to anchor the concept.
• Code: 10–30 lines. Comment the non-obvious parts only.
• Include 2–3 progressively more real examples.
• Summarise in 3 key takeaways at the end.
• Light tradeoffs are OK but don't overwhelm.
""",
    3: """
[ADAPTIVE LEVEL: 🟡 Practitioner — Bloom's Level 3: APPLY]
Respond as a senior software engineer pair-programming with a mid-level developer.
• Give working, production-pattern code immediately.
• Explain WHAT + HOW + WHY this approach is correct.
• Code: 30–100 lines. Use real-world patterns (repositories, services, error handling).
• One complete, runnable example is worth more than three toy snippets.
• Surface 1–2 key tradeoffs. Mention one common mistake to avoid.
• Format: Brief intro → Code → Explanation → What to do next.
""",
    4: """
[ADAPTIVE LEVEL: 🟠 Advanced — Bloom's Level 4: ANALYSE]
Respond as a principal engineer reviewing with a senior engineer.
• Go deep. Compare 2–3 architectural approaches with explicit tradeoffs.
• Show the anti-patterns alongside the recommended pattern.
• Code: 100+ lines, production-grade. Include type annotations, error handling, logging.
• Surface the system-level implications: performance, scalability, maintainability.
• Use engineering first-principles: CAP theorem, SOLID, Hyrum's Law where relevant.
• Format: Architecture analysis → Code comparison → Recommendation → Risk matrix.
""",
    5: """
[ADAPTIVE LEVEL: 🔴 Expert — Bloom's Level 5: EVALUATE]
Respond as a Distinguished Engineer reviewing with a tech lead.
• Be ruthlessly precise. No hand-waving. Cite principles, benchmarks, or trade papers.
• Critique existing approaches. Justify your recommendation with evidence.
• Code: Full production-grade system. TDD. Security hardened. Observable. Typed.
• Surface hidden costs: operational complexity, cognitive overhead, team friction.
• Include ADR-style decision record: Context → Options → Decision → Consequences.
• Format: Critical assessment → Evidence → Recommended approach → Migration path.
""",
    6: """
[ADAPTIVE LEVEL: 🟣 Visionary — Bloom's Level 6: CREATE]
Respond as a CTO & Chief Architect designing for a unicorn-scale platform.
• Autonomously create the full system: PRD → Architecture → Code → Tests → DevOps.
• Design like Apple (elegance), build like Google (reliability), ship like Netflix (speed).
• Synthesize original solutions. Do not just implement existing patterns — improve them.
• Deliverables: 💻 Multi-file production code + 📐 C4 Architecture + 👁️ Live preview.
• Apply all 24 engineering skills: spec → TDD → security → performance → observability.
• This is LOT AI at full ASI-grade. No shortcuts. No boilerplate. Pure excellence.
""",
}


def detect_bloom_level_from_message(message: str, user_overall_level: str = "intermediate") -> Tuple[int, str]:
    """
    Infer the most appropriate Bloom's level for a user message.
    Returns: (bloom_level, reasoning)
    """
    msg_lower = message.lower()

    # Level 6 signals — system design, build from scratch
    level6_keywords = [
        "build me", "create a full", "design a system", "architect", "from scratch",
        "end-to-end", "full platform", "saas", "production-ready entire", "full stack app",
        "complete system", "startup idea", "build an ai"
    ]
    # Level 5 signals — critique, optimise, evaluate
    level5_keywords = [
        "is this good", "review my", "optimise", "critique", "is this the best",
        "what's wrong with", "improve this", "evaluate", "assess", "should i use",
        "best approach", "justify"
    ]
    # Level 4 signals — compare, analyse, tradeoffs
    level4_keywords = [
        "compare", "vs", "versus", "tradeoffs", "which is better", "difference between",
        "why not", "when to use", "pros and cons", "differentiate", "analyse"
    ]
    # Level 3 signals — implement, apply, use
    level3_keywords = [
        "how to implement", "write code", "build a", "create a", "make a", "add feature",
        "implement", "develop", "code for", "example of", "show me how", "step by step"
    ]
    # Level 2 signals — understand, explain
    level2_keywords = [
        "explain", "what is", "how does", "describe", "tell me about", "what does",
        "why does", "how do", "what are"
    ]
    # Level 1 signals — recall, define
    level1_keywords = [
        "define", "what's the meaning", "give me a list", "name the", "what does * stand for"
    ]

    # Check signals in reverse order (high → low) for priority
    for keyword in level6_keywords:
        if keyword in msg_lower:
            return 6, f"Detected 'Create' intent: '{keyword}'"
    for keyword in level5_keywords:
        if keyword in msg_lower:
            return 5, f"Detected 'Evaluate' intent: '{keyword}'"
    for keyword in level4_keywords:
        if keyword in msg_lower:
            return 4, f"Detected 'Analyse' intent: '{keyword}'"
    for keyword in level3_keywords:
        if keyword in msg_lower:
            return 3, f"Detected 'Apply' intent: '{keyword}'"
    for keyword in level2_keywords:
        if keyword in msg_lower:
            return 2, f"Detected 'Understand' intent: '{keyword}'"
    for keyword in level1_keywords:
        if keyword in msg_lower:
            return 1, f"Detected 'Remember' intent: '{keyword}'"

    # Fallback: map overall_level to a default Bloom's level
    level_map = {
        "beginner": 2,
        "intermediate": 3,
        "advanced": 4,
        "expert": 5,
    }
    default_level = level_map.get(user_overall_level, 3)
    return default_level, f"Defaulting to level {default_level} for '{user_overall_level}' user"


def get_bloom_system_prompt(bloom_level: int) -> str:
    """Return the system prompt injection for a specific Bloom's level."""
    return BLOOM_PROMPT_TEMPLATES.get(bloom_level, BLOOM_PROMPT_TEMPLATES[3])


def get_bloom_meta(bloom_level: int) -> Dict:
    """Return metadata dict for the Bloom's level."""
    return BLOOM_LEVEL_META.get(bloom_level, BLOOM_LEVEL_META[3])


def inject_bloom_taxonomy_prompt(system_prompt: str, bloom_level: int) -> str:
    """
    Inject the Bloom's Taxonomy level directive into the system prompt.
    This is the primary integration point with api_real.py.
    """
    bloom_injection = get_bloom_system_prompt(bloom_level)
    meta = get_bloom_meta(bloom_level)
    header = f"\n\n[🎓 LOTAI ADAPTIVE BLOOM ENGINE — Level {bloom_level}: {meta['name'].upper()}]:\n"
    return system_prompt + header + bloom_injection
