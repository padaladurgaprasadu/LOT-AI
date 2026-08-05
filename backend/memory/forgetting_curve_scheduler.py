"""
LOT AI Forgetting Curve Scheduler v1.0
========================================
Implements the Ebbinghaus Forgetting Curve with spaced repetition scheduling
to help users retain knowledge at scientifically optimal review intervals.

Hermann Ebbinghaus discovered (1885) that memory decays exponentially:
  After 20 min: 58% retained
  After 1 hour:  44% retained
  After 1 day:   33% retained
  After 7 days:  23% retained
  After 30 days: 21% retained

Spaced Repetition (SR) counteracts decay by reviewing at optimal intervals:
  Review 1: After 1 hour       → Retention jumps to ~90%
  Review 2: After 24 hours     → Retention stays at ~80%
  Review 3: After 3 days       → Retention stays at ~85%
  Review 4: After 7 days       → Retention stays at ~87%
  Review 5: After 30 days      → Retention stays at ~90%

LOT AI integration:
  • Every concept explained is registered in the user's profile
  • When the user returns, LOT AI proactively surfaces concepts due for review
  • "Quick recall check" prompts reinforce learning without being intrusive
  • Mastery score (0.0–1.0) tracks per-concept retention strength
"""

import time
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# Spaced repetition intervals in seconds
SR_INTERVALS = [
    3600,        # 1 hour
    86400,       # 1 day
    259200,      # 3 days
    604800,      # 7 days
    2592000,     # 30 days
    7776000,     # 90 days  (mastered)
]

# Minimum mastery score to advance to next interval
MASTERY_THRESHOLD = 0.7

# Concepts due within this window (seconds) are surfaced as review suggestions
REVIEW_WINDOW_SECONDS = 3600  # 1 hour


class ForgettingCurveScheduler:
    """
    Manages spaced repetition schedule for a user's learned concepts.
    Works in conjunction with UserIntelligenceProfile.
    """

    def __init__(self, learned_concepts: Dict):
        """
        Args:
            learned_concepts: Dict from UserIntelligenceProfile._data["learned_concepts"]
                Format: { concept_name: { first_seen, last_seen, review_count, mastery_score, interval_index } }
        """
        self.concepts = learned_concepts

    def register_concept(self, concept: str) -> None:
        """Register a newly encountered concept for future spaced repetition."""
        if concept not in self.concepts:
            now = time.time()
            self.concepts[concept] = {
                "first_seen": now,
                "last_seen": now,
                "review_count": 0,
                "mastery_score": 0.2,
                "interval_index": 0,  # Start at interval[0] = 1 hour
                "next_review": now + SR_INTERVALS[0],
            }

    def record_review(self, concept: str, success: bool) -> None:
        """
        Record a review session for a concept.
        If successful: advance to next interval. If not: reset to beginning.
        """
        if concept not in self.concepts:
            self.register_concept(concept)
            return

        entry = self.concepts[concept]
        now = time.time()
        entry["last_seen"] = now
        entry["review_count"] = entry.get("review_count", 0) + 1

        if success:
            # Advance to next interval (up to max)
            idx = min(entry.get("interval_index", 0) + 1, len(SR_INTERVALS) - 1)
            entry["interval_index"] = idx
            entry["mastery_score"] = min(1.0, entry.get("mastery_score", 0.2) + 0.15)
            entry["next_review"] = now + SR_INTERVALS[idx]
        else:
            # Reset to first interval
            entry["interval_index"] = 0
            entry["mastery_score"] = max(0.0, entry.get("mastery_score", 0.2) - 0.1)
            entry["next_review"] = now + SR_INTERVALS[0]

    def get_due_concepts(self, max_items: int = 5) -> List[Tuple[str, float]]:
        """
        Return concepts that are due for review right now.
        Returns: List of (concept_name, mastery_score) sorted by most overdue first.
        """
        now = time.time()
        due = []
        for concept, entry in self.concepts.items():
            next_review = entry.get("next_review", 0)
            if now >= next_review:
                overdue_by = now - next_review
                mastery = entry.get("mastery_score", 0.2)
                due.append((concept, mastery, overdue_by))

        # Sort by most overdue first, then by lowest mastery
        due.sort(key=lambda x: (-x[2], x[1]))
        return [(name, mastery) for name, mastery, _ in due[:max_items]]

    def get_mastery_score(self, concept: str) -> float:
        """Return current mastery score for a concept (0.0–1.0)."""
        return self.concepts.get(concept, {}).get("mastery_score", 0.0)

    def get_next_review_time(self, concept: str) -> Optional[float]:
        """Return unix timestamp of next scheduled review for a concept."""
        return self.concepts.get(concept, {}).get("next_review")

    def get_learning_summary(self) -> Dict:
        """Generate a learning progress summary for dashboard display."""
        now = time.time()
        total = len(self.concepts)
        mastered = sum(1 for c in self.concepts.values() if c.get("mastery_score", 0) >= 0.9)
        learning = sum(1 for c in self.concepts.values() if 0.3 <= c.get("mastery_score", 0) < 0.9)
        new_items = sum(1 for c in self.concepts.values() if c.get("mastery_score", 0) < 0.3)
        due_count = len(self.get_due_concepts(max_items=100))

        avg_mastery = 0.0
        if total > 0:
            avg_mastery = sum(c.get("mastery_score", 0) for c in self.concepts.values()) / total

        return {
            "total_concepts": total,
            "mastered_count": mastered,
            "learning_count": learning,
            "new_count": new_items,
            "due_for_review": due_count,
            "average_mastery_pct": round(avg_mastery * 100, 1),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def generate_review_prompt_block(self, max_items: int = 3) -> str:
        """
        Generate a proactive review prompt block to inject into LOT AI responses.
        Returns empty string if no concepts are due for review.
        """
        due = self.get_due_concepts(max_items=max_items)
        if not due:
            return ""

        lines = ["\n\n[📚 LOTAI ADAPTIVE RECALL — Concepts Due for Review]:"]
        lines.append("These concepts are ready to reinforce in your long-term memory:\n")
        for concept, mastery in due:
            bars = int(mastery * 10)
            bar = "█" * bars + "░" * (10 - bars)
            pct = int(mastery * 100)
            lines.append(f"  • **{concept.replace('_', ' ').title()}** — Mastery: [{bar}] {pct}%")
        lines.append("\nWant a quick recall challenge on any of these? Just ask!")
        return "\n".join(lines)


def inject_forgetting_curve_prompt(system_prompt: str, learned_concepts: Dict) -> str:
    """
    Inject spaced repetition review suggestions into the system prompt
    if any concepts are due for review.
    """
    scheduler = ForgettingCurveScheduler(learned_concepts)
    due = scheduler.get_due_concepts(max_items=3)
    if not due:
        return system_prompt

    review_block = "\n\n[📚 FORGETTING CURVE SCHEDULER — Proactive Review]:\n"
    review_block += "The following concepts are due for spaced repetition review. "
    review_block += "Weave a brief recall check into your response if contextually relevant:\n"
    for concept, mastery in due:
        review_block += f"  • {concept.replace('_', ' ').title()} (mastery: {int(mastery * 100)}%)\n"

    return system_prompt + review_block
