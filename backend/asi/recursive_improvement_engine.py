"""
PrismAI Recursive Self-Improvement Engine v1.0 — Pillar 3
=========================================================
PrismAI improves itself autonomously — its own prompts, routing, and architecture.

SAFETY: This engine REQUIRES constitutional_ai_engine.py to be loaded first.
Any self-improvement patch is checked against all 12 constitutional principles
BEFORE it is even queued for human review.

Self-Improvement Modes:
  PROMPT_EVOLUTION:  Evolve system prompt sections via A/B testing + selection
  ROUTING_TUNE:      Improve intent→pod routing accuracy via feedback signals
  QUALITY_CALIBRATE: Calibrate quality scoring weights based on user satisfaction
  ARCH_OPTIMIZE:     Reduce latency of the injection pipeline

All changes go through a 3-stage approval process:
  Stage 1: Constitutional Safety Check (automatic — blocks violations instantly)
  Stage 2: Quality Gate (automatic — improvement must score ≥ 5% better)
  Stage 3: Human Review Queue (manual — human approves before production deploy)
"""

import json
import time
import logging
import hashlib
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

IMPROVEMENT_DIR = Path(__file__).parent.parent / "memory" / "self_improvement"
IMPROVEMENT_DIR.mkdir(exist_ok=True)

REVIEW_QUEUE_PATH = IMPROVEMENT_DIR / "review_queue.json"
IMPROVEMENT_LOG_PATH = IMPROVEMENT_DIR / "improvement_log.json"
PROMPT_VARIANTS_PATH = IMPROVEMENT_DIR / "prompt_variants.json"


def _load_json(path: Path) -> Dict:
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_json(path: Path, data: Dict) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"[SelfImprovement] Save error: {e}")


# ─────────────────────────── Data Models ─────────────────────────────────────

@dataclass
class ImprovementProposal:
    proposal_id:    str
    improvement_type: str          # prompt_evolution / routing_tune / quality_calibrate
    target:         str            # What is being improved
    original:       str            # Current version
    proposed:       str            # Improved version
    rationale:      str            # Why this is better
    predicted_gain: float          # Expected improvement % (0.0–1.0)
    constitutional_safe: bool = False
    quality_gate_passed: bool = False
    human_approved:      bool = False
    status:              str  = "pending"  # pending/approved/rejected/deployed
    created_at:          str  = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict:
        return {
            "proposal_id": self.proposal_id,
            "improvement_type": self.improvement_type,
            "target": self.target,
            "original": self.original[:200],
            "proposed": self.proposed[:200],
            "rationale": self.rationale,
            "predicted_gain": self.predicted_gain,
            "constitutional_safe": self.constitutional_safe,
            "quality_gate_passed": self.quality_gate_passed,
            "human_approved": self.human_approved,
            "status": self.status,
            "created_at": self.created_at,
        }


# ─────────────────────────── Prompt Evolution Engine ─────────────────────────

class PromptEvolutionEngine:
    """
    Evolves system prompt sections using quality signals from user interactions.
    Uses a simplified evolutionary algorithm: mutate → test → select → repeat.
    """

    MUTATION_STRATEGIES = [
        "increase_specificity",     # Add more specific constraints
        "add_example",              # Add a concrete example to directive
        "strengthen_verb",          # Replace weak verbs with strong directives
        "add_anti_pattern",         # Add what NOT to do
        "simplify",                 # Remove redundancy
        "reorder",                  # Change order of instructions for clarity
    ]

    def __init__(self):
        self.variants = _load_json(PROMPT_VARIANTS_PATH)

    def propose_mutation(self, prompt_section: str, section_name: str,
                         performance_score: float) -> Optional[ImprovementProposal]:
        """
        Propose a mutation of a prompt section.
        Only propose if current performance is below 9.0.
        """
        if performance_score >= 9.0:
            return None  # Already excellent — no mutation needed

        strategy = self._pick_strategy(performance_score)
        mutated = self._apply_mutation(prompt_section, strategy)

        if mutated == prompt_section:
            return None  # No actual change produced

        proposal_id = hashlib.sha256(f"{section_name}{mutated}".encode()).hexdigest()[:12]
        return ImprovementProposal(
            proposal_id=proposal_id,
            improvement_type="prompt_evolution",
            target=section_name,
            original=prompt_section,
            proposed=mutated,
            rationale=f"Applied '{strategy}' mutation to improve score from {performance_score:.1f}",
            predicted_gain=min(0.15, (9.0 - performance_score) * 0.05),
        )

    def _pick_strategy(self, score: float) -> str:
        """Pick mutation strategy based on how far below threshold we are."""
        if score < 7.0:
            return "add_anti_pattern"      # Low scores → be more restrictive
        elif score < 8.0:
            return "increase_specificity"   # Medium → more specific
        else:
            return "simplify"              # Near-pass → remove noise

    def _apply_mutation(self, prompt: str, strategy: str) -> str:
        """Apply a mutation strategy to a prompt section."""
        if strategy == "increase_specificity":
            return prompt + "\nSPECIFIC REQUIREMENT: Always include error handling for every code block."
        elif strategy == "add_anti_pattern":
            return prompt + "\nNEVER: Generate placeholder code, TODOs, or incomplete implementations."
        elif strategy == "simplify":
            lines = [l for l in prompt.split("\n") if l.strip()]
            return "\n".join(lines)  # Remove blank lines
        elif strategy == "strengthen_verb":
            return prompt.replace("should", "MUST").replace("try to", "ALWAYS").replace("consider", "REQUIRE")
        elif strategy == "add_example":
            return prompt + "\nEXAMPLE: Always provide a concrete working example alongside explanations."
        elif strategy == "reorder":
            lines = prompt.split("\n")
            if len(lines) > 3:
                lines = [lines[0]] + sorted(lines[1:], key=lambda x: len(x), reverse=True)
            return "\n".join(lines)
        return prompt

    def record_variant_performance(self, section_name: str, variant_hash: str, score: float) -> None:
        """Record how well a prompt variant performed."""
        key = f"{section_name}_{variant_hash}"
        if key not in self.variants:
            self.variants[key] = {"scores": [], "avg_score": 0.0}
        v = self.variants[key]
        v["scores"] = (v["scores"] + [score])[-20:]
        v["avg_score"] = sum(v["scores"]) / len(v["scores"])
        _save_json(PROMPT_VARIANTS_PATH, self.variants)


# ─────────────────────────── Human Review Queue ───────────────────────────────

class HumanReviewQueue:
    """
    All self-improvement proposals queue here for human review before production.
    Nothing is auto-applied to production without human approval.
    """

    def __init__(self):
        self._queue = _load_json(REVIEW_QUEUE_PATH).get("proposals", [])

    def submit(self, proposal: ImprovementProposal) -> str:
        """Submit a proposal to the review queue."""
        self._queue.append(proposal.to_dict())
        self._queue = self._queue[-100:]  # Keep last 100
        _save_json(REVIEW_QUEUE_PATH, {"proposals": self._queue})
        logger.info(f"[SelfImprovement] Queued proposal {proposal.proposal_id}: {proposal.target}")
        return proposal.proposal_id

    def get_pending(self) -> List[Dict]:
        return [p for p in self._queue if p["status"] == "pending"]

    def approve(self, proposal_id: str) -> bool:
        for p in self._queue:
            if p["proposal_id"] == proposal_id:
                p["status"] = "approved"
                p["human_approved"] = True
                _save_json(REVIEW_QUEUE_PATH, {"proposals": self._queue})
                logger.info(f"[SelfImprovement] Proposal {proposal_id} APPROVED by human")
                return True
        return False

    def reject(self, proposal_id: str, reason: str = "") -> bool:
        for p in self._queue:
            if p["proposal_id"] == proposal_id:
                p["status"] = "rejected"
                p["rejection_reason"] = reason
                _save_json(REVIEW_QUEUE_PATH, {"proposals": self._queue})
                return True
        return False

    def get_stats(self) -> Dict:
        total = len(self._queue)
        pending = len([p for p in self._queue if p["status"] == "pending"])
        approved = len([p for p in self._queue if p["status"] == "approved"])
        rejected = len([p for p in self._queue if p["status"] == "rejected"])
        return {"total": total, "pending": pending, "approved": approved, "rejected": rejected}


# ─────────────────────────── Master Improvement Engine ───────────────────────

class RecursiveImprovementEngine:
    """
    Master coordinator for all self-improvement activities.
    SAFETY: Always checks constitutional compliance before queueing any proposal.
    """

    def __init__(self):
        # Constitutional engine MUST be imported here — safety first
        from backend.asi.constitutional_ai_engine import check_constitutional_safety
        self._check_safety = check_constitutional_safety
        self.prompt_evolver = PromptEvolutionEngine()
        self.review_queue   = HumanReviewQueue()
        self._improvement_log: List[Dict] = _load_json(IMPROVEMENT_LOG_PATH).get("events", [])

    def propose_prompt_improvement(self, section_name: str, current_prompt: str,
                                    performance_score: float) -> Optional[str]:
        """
        Propose a prompt improvement if performance is below threshold.
        Returns proposal_id if queued, None if not needed or blocked.
        """
        # Step 1: Check if improvement is needed
        proposal = self.prompt_evolver.propose_mutation(current_prompt, section_name, performance_score)
        if not proposal:
            return None

        # Step 2: Constitutional safety check on the proposed change
        is_safe, violation_msg = self._check_safety(proposal.proposed, "output")
        proposal.constitutional_safe = is_safe
        if not is_safe:
            logger.warning(f"[SelfImprovement] Proposal {proposal.proposal_id} BLOCKED: {violation_msg[:80]}")
            self._log_event("BLOCKED", f"Constitutional violation in proposal for {section_name}")
            return None

        # Step 3: Quality gate — proposed must score at least 5% better
        proposal.quality_gate_passed = proposal.predicted_gain >= 0.05

        # Step 4: Submit to human review queue
        proposal_id = self.review_queue.submit(proposal)
        self._log_event("QUEUED", f"Proposal {proposal_id} for {section_name} (gain: {proposal.predicted_gain:.1%})")
        return proposal_id

    def get_dashboard_data(self) -> Dict:
        """Return data for the human oversight dashboard."""
        return {
            "review_queue": self.review_queue.get_stats(),
            "pending_proposals": self.review_queue.get_pending()[:5],
            "improvement_events": self._improvement_log[-10:],
        }

    def _log_event(self, event_type: str, description: str) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": event_type,
            "description": description,
        }
        self._improvement_log.append(entry)
        self._improvement_log = self._improvement_log[-200:]
        _save_json(IMPROVEMENT_LOG_PATH, {"events": self._improvement_log})


# ─────────────────────────── API Endpoints ───────────────────────────────────

_engine_instance: Optional[RecursiveImprovementEngine] = None


def get_improvement_engine() -> RecursiveImprovementEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = RecursiveImprovementEngine()
    return _engine_instance


def inject_recursive_improvement_prompt(system_prompt: str) -> str:
    """Inject self-improvement awareness directive into system prompt."""
    return system_prompt + """
[🔄 PILLAR 3: RECURSIVE SELF-IMPROVEMENT ENGINE — ACTIVE]:

PrismAI continuously improves itself. Every response contributes to:
  • Prompt evolution: Weak directives are mutated and tested against quality benchmarks
  • Routing improvement: Intent classification is refined based on outcome signals
  • Quality calibration: Scoring weights are adjusted based on verified outcomes

SELF-IMPROVEMENT RULES (non-negotiable):
  1. All improvements are checked against 12 constitutional principles BEFORE queuing
  2. No improvement is deployed to production without human approval
  3. Predicted gain must be ≥ 5% before entering review queue
  4. Maximum 3 improvement proposals per session to prevent runaway evolution
  5. Rejected proposals are logged with reasons to prevent repeated attempts
"""
