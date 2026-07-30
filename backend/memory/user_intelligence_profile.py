"""
PrismAI User Intelligence Profile v1.0
=======================================
Persistent per-user knowledge graph that tracks:
  • Domain expertise levels (0–10 per domain)
  • Preferred technology stack
  • Learning velocity (fast / medium / slow)
  • Bloom's Taxonomy tier per domain
  • Session history, project names, and architectural decisions
  • Code style preferences extracted from user edits
  • Correction patterns (what user changed from PrismAI's code)
  • Spaced repetition schedule per concept

This module is storage-agnostic: profiles are persisted as JSON files
in backend/memory/profiles/<user_id>.json and loaded on each request.

Design Principles:
  1. Privacy-first: No sensitive data stored, only learning signals
  2. Graceful degradation: If profile missing, start with neutral defaults
  3. Continuous update: Every interaction refines the profile
  4. Transparent: User can inspect or reset their profile at any time
"""

import json
import os
import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# Storage directory for user profiles
PROFILES_DIR = Path(__file__).parent / "profiles"
PROFILES_DIR.mkdir(exist_ok=True)

# Default expertise level for all domains (0 = none, 10 = world-class expert)
DEFAULT_EXPERTISE_LEVEL = 3

# Supported domains for expertise tracking
KNOWLEDGE_DOMAINS = [
    # Core Engineering
    "python", "javascript", "typescript", "rust", "go", "java", "c_cpp",
    # Frontend
    "react", "nextjs", "vue", "angular", "html_css", "webgl", "threejs",
    # Backend
    "fastapi", "nodejs", "django", "graphql", "grpc", "microservices",
    # Data & AI
    "machine_learning", "deep_learning", "llm_engineering", "data_science",
    "sql", "postgresql", "redis", "mongodb", "vector_databases",
    # DevOps & Cloud
    "docker", "kubernetes", "terraform", "github_actions", "aws", "gcp", "azure",
    # Specialised
    "cybersecurity", "blockchain", "embedded_systems", "biotech", "fintech",
    "space_engineering", "ece_vlsi", "eee_power", "pcb_design",
    # Soft Skills
    "system_design", "architecture", "product_management", "data_analysis"
]

# Bloom's Taxonomy levels
BLOOM_LEVELS = {
    1: "Remember",    # Can recall facts and concepts
    2: "Understand",  # Can explain ideas in own words
    3: "Apply",       # Can use knowledge in new situations
    4: "Analyse",     # Can draw connections, compare approaches
    5: "Evaluate",    # Can justify decisions, critique solutions
    6: "Create",      # Can build novel original solutions
}


class UserIntelligenceProfile:
    """
    Represents a single user's adaptive learning profile.
    All interactions update this profile to personalise future responses.
    """

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.profile_path = PROFILES_DIR / f"{user_id}.json"
        self._data: Dict[str, Any] = self._load_or_create()

    # ─────────────────────────── Load / Save ───────────────────────────────

    def _load_or_create(self) -> Dict[str, Any]:
        """Load existing profile or create a fresh default one."""
        if self.profile_path.exists():
            try:
                with open(self.profile_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                logger.info(f"[AdaptiveLearning] Loaded profile for user: {self.user_id}")
                return data
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"[AdaptiveLearning] Corrupted profile, recreating: {e}")

        return self._create_default_profile()

    def _create_default_profile(self) -> Dict[str, Any]:
        """Create a blank default user profile with neutral assumptions."""
        now = datetime.now(timezone.utc).isoformat()
        profile = {
            "user_id": self.user_id,
            "created_at": now,
            "last_seen": now,
            "session_count": 0,

            # Expertise levels: 0–10 per domain
            "expertise": {domain: DEFAULT_EXPERTISE_LEVEL for domain in KNOWLEDGE_DOMAINS},

            # Bloom's Taxonomy tier per domain (1–6)
            "bloom_tier": {domain: 2 for domain in KNOWLEDGE_DOMAINS},  # Default: Understand

            # Inferred overall expertise category
            "overall_level": "intermediate",  # beginner / intermediate / advanced / expert

            # Preferred tech stack detected from conversations
            "preferred_stack": [],

            # Learning velocity: how fast the user picks up new concepts
            "learning_velocity": "medium",  # slow / medium / fast

            # Response format preferences
            "format_preference": "balanced",  # code_heavy / text_heavy / balanced / visual

            # Projects the user has worked on with PrismAI
            "projects": [],

            # Architectural decisions recorded as ADRs
            "architecture_decisions": [],

            # Code style patterns extracted from user edits
            "code_style": {
                "indentation": "spaces_4",
                "naming_convention": "unknown",    # camelCase / snake_case / PascalCase
                "prefers_types": None,              # True = typed code, False = dynamic
                "prefers_comments": True,
                "prefers_tests": True,
            },

            # Topics the user has covered (for spaced repetition)
            "learned_concepts": {},  # concept → {last_seen, review_count, mastery_score}

            # Correction history: what the user changed in PrismAI's responses
            "correction_patterns": [],

            # Interaction signals
            "thumbs_up_count": 0,
            "thumbs_down_count": 0,
            "edit_count": 0,
        }
        self._save(profile)
        return profile

    def _save(self, data: Optional[Dict] = None) -> None:
        """Persist the profile to disk."""
        d = data or self._data
        d["last_seen"] = datetime.now(timezone.utc).isoformat()
        try:
            with open(self.profile_path, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
        except OSError as e:
            logger.error(f"[AdaptiveLearning] Failed to save profile: {e}")

    # ─────────────────────────── Getters ───────────────────────────────────

    @property
    def overall_level(self) -> str:
        return self._data.get("overall_level", "intermediate")

    @property
    def preferred_stack(self) -> List[str]:
        return self._data.get("preferred_stack", [])

    @property
    def learning_velocity(self) -> str:
        return self._data.get("learning_velocity", "medium")

    @property
    def format_preference(self) -> str:
        return self._data.get("format_preference", "balanced")

    def get_expertise(self, domain: str) -> int:
        return self._data.get("expertise", {}).get(domain, DEFAULT_EXPERTISE_LEVEL)

    def get_bloom_tier(self, domain: str) -> int:
        return self._data.get("bloom_tier", {}).get(domain, 2)

    def get_bloom_label(self, domain: str) -> str:
        tier = self.get_bloom_tier(domain)
        return BLOOM_LEVELS.get(tier, "Understand")

    def get_top_domains(self, n: int = 5) -> List[str]:
        """Return the n domains with highest expertise scores."""
        expertise = self._data.get("expertise", {})
        return sorted(expertise, key=lambda d: expertise[d], reverse=True)[:n]

    # ─────────────────────────── Updaters ──────────────────────────────────

    def record_session(self, user_message: str, topics: List[str]) -> None:
        """Record a new session and update related domain signals."""
        self._data["session_count"] = self._data.get("session_count", 0) + 1
        self._data["last_seen"] = datetime.now(timezone.utc).isoformat()

        # Update learned concepts for spaced repetition
        now_ts = time.time()
        learned = self._data.setdefault("learned_concepts", {})
        for topic in topics:
            if topic not in learned:
                learned[topic] = {"first_seen": now_ts, "last_seen": now_ts, "review_count": 0, "mastery_score": 0.3}
            else:
                learned[topic]["last_seen"] = now_ts
                learned[topic]["review_count"] += 1
                # Increase mastery incrementally with each review
                learned[topic]["mastery_score"] = min(1.0, learned[topic]["mastery_score"] + 0.1)

        self._save()

    def upgrade_expertise(self, domain: str, delta: float = 0.5) -> None:
        """Slightly increase expertise in a domain based on demonstrated understanding."""
        if domain in KNOWLEDGE_DOMAINS:
            current = self._data["expertise"].get(domain, DEFAULT_EXPERTISE_LEVEL)
            self._data["expertise"][domain] = min(10.0, current + delta)
            self._recalculate_bloom_tier(domain)
            self._recalculate_overall_level()
            self._save()

    def downgrade_expertise(self, domain: str, delta: float = 0.2) -> None:
        """Slightly decrease expertise if user struggles repeatedly in a domain."""
        if domain in KNOWLEDGE_DOMAINS:
            current = self._data["expertise"].get(domain, DEFAULT_EXPERTISE_LEVEL)
            self._data["expertise"][domain] = max(0.0, current - delta)
            self._recalculate_bloom_tier(domain)
            self._recalculate_overall_level()
            self._save()

    def _recalculate_bloom_tier(self, domain: str) -> None:
        """Map expertise score (0–10) to Bloom's tier (1–6)."""
        score = self._data["expertise"].get(domain, DEFAULT_EXPERTISE_LEVEL)
        if score < 2:
            tier = 1  # Remember
        elif score < 4:
            tier = 2  # Understand
        elif score < 5.5:
            tier = 3  # Apply
        elif score < 7:
            tier = 4  # Analyse
        elif score < 9:
            tier = 5  # Evaluate
        else:
            tier = 6  # Create
        self._data["bloom_tier"][domain] = tier

    def _recalculate_overall_level(self) -> None:
        """Recalculate overall level from average expertise across top domains."""
        expertise_values = list(self._data.get("expertise", {}).values())
        if not expertise_values:
            return
        avg = sum(expertise_values) / len(expertise_values)
        if avg < 3:
            self._data["overall_level"] = "beginner"
        elif avg < 5.5:
            self._data["overall_level"] = "intermediate"
        elif avg < 8:
            self._data["overall_level"] = "advanced"
        else:
            self._data["overall_level"] = "expert"

    def record_correction(self, original_code: str, corrected_code: str) -> None:
        """Record what the user changed from PrismAI's code to learn style preferences."""
        patterns = self._data.setdefault("correction_patterns", [])
        patterns.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "original_length": len(original_code),
            "corrected_length": len(corrected_code),
            "change_ratio": abs(len(corrected_code) - len(original_code)) / max(1, len(original_code))
        })
        # Keep only last 50 corrections
        self._data["correction_patterns"] = patterns[-50:]
        self._data["edit_count"] = self._data.get("edit_count", 0) + 1
        self._save()

    def record_feedback(self, positive: bool) -> None:
        """Record a thumbs up/down signal."""
        if positive:
            self._data["thumbs_up_count"] = self._data.get("thumbs_up_count", 0) + 1
        else:
            self._data["thumbs_down_count"] = self._data.get("thumbs_down_count", 0) + 1
        self._save()

    def detect_stack_from_message(self, message: str) -> None:
        """Detect technology preferences from what the user mentions."""
        stack_keywords = {
            "react": "React", "nextjs": "Next.js", "vue": "Vue.js",
            "angular": "Angular", "svelte": "Svelte",
            "python": "Python", "fastapi": "FastAPI", "django": "Django",
            "nodejs": "Node.js", "express": "Express.js",
            "typescript": "TypeScript", "javascript": "JavaScript", "rust": "Rust",
            "postgresql": "PostgreSQL", "mysql": "MySQL", "mongodb": "MongoDB",
            "redis": "Redis", "docker": "Docker", "kubernetes": "Kubernetes",
            "aws": "AWS", "gcp": "GCP", "azure": "Azure",
            "tailwind": "TailwindCSS", "graphql": "GraphQL", "grpc": "gRPC",
        }
        msg_lower = message.lower()
        stack = self._data.setdefault("preferred_stack", [])
        for key, label in stack_keywords.items():
            if key in msg_lower and label not in stack:
                stack.append(label)
        # Keep top 10 most recently detected
        self._data["preferred_stack"] = stack[-10:]
        self._save()

    def to_context_dict(self) -> Dict[str, Any]:
        """Return a minimal context dict suitable for prompt injection."""
        return {
            "overall_level": self.overall_level,
            "preferred_stack": self.preferred_stack[:5],
            "learning_velocity": self.learning_velocity,
            "format_preference": self.format_preference,
            "top_domains": self.get_top_domains(5),
            "session_count": self._data.get("session_count", 0),
            "bloom_summary": {
                domain: self.get_bloom_label(domain)
                for domain in self.get_top_domains(5)
            }
        }


def load_profile(user_id: str = "default") -> UserIntelligenceProfile:
    """Convenience function to load or create a user intelligence profile."""
    return UserIntelligenceProfile(user_id)
