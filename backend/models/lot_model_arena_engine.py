"""
LOT Model Arena Engine v1.0 — Multi-Model Comparison & Routing
==============================================================
Backend engine for the LOT Model Arena dashboard.
Provides model registry, benchmark data, token counting,
session management, and auto-fallback routing.
"""

import os
import json
import time
import uuid
from typing import Dict, List, Any, Optional
from backend.utils.logger import get_logger

logger = get_logger(__name__)


# LOT Model Registry — replaces Claude Opus/Fable/Sonnet/Haiku lineup
LOT_MODEL_REGISTRY = {
    "lot-sovereign-ultra": {
        "name": "LOT Sovereign Ultra",
        "description": "Flagship 1M-context reasoning model",
        "context_window": 1000000,
        "speed_rating": "Medium",
        "tokens_per_sec": 85,
        "accent_color": "#38bdf8",
        "tier": "flagship",
        "benchmarks": {
            "swe_bench": 72.8,
            "gpqa_diamond": 78.4,
            "math_500": 96.2,
            "multimodal": True,
            "agentic_tasks": 94.1
        }
    },
    "lot-prometheus-550b": {
        "name": "LOT Prometheus 550B",
        "description": "Deep reasoning & long-horizon planning",
        "context_window": 512000,
        "speed_rating": "Slow",
        "tokens_per_sec": 45,
        "accent_color": "#a855f7",
        "tier": "premium",
        "benchmarks": {
            "swe_bench": 68.5,
            "gpqa_diamond": 82.1,
            "math_500": 97.8,
            "multimodal": True,
            "agentic_tasks": 91.3
        }
    },
    "lot-nemotron-flash": {
        "name": "LOT Nemotron Flash",
        "description": "Fast daily coding & lightweight tasks",
        "context_window": 200000,
        "speed_rating": "Fast",
        "tokens_per_sec": 220,
        "accent_color": "#22c55e",
        "tier": "standard",
        "benchmarks": {
            "swe_bench": 61.2,
            "gpqa_diamond": 64.8,
            "math_500": 88.4,
            "multimodal": True,
            "agentic_tasks": 78.6
        }
    },
    "lot-architect-70b": {
        "name": "LOT Architect 70B",
        "description": "Code architecture & system design",
        "context_window": 128000,
        "speed_rating": "Medium",
        "tokens_per_sec": 140,
        "accent_color": "#f59e0b",
        "tier": "standard",
        "benchmarks": {
            "swe_bench": 58.9,
            "gpqa_diamond": 60.2,
            "math_500": 82.1,
            "multimodal": False,
            "agentic_tasks": 72.4
        }
    },
    "lot-haiku-lite": {
        "name": "LOT Haiku Lite",
        "description": "Lightweight utility model",
        "context_window": 64000,
        "speed_rating": "Ultra Fast",
        "tokens_per_sec": 380,
        "accent_color": "#ec4899",
        "tier": "lite",
        "benchmarks": {
            "swe_bench": 42.1,
            "gpqa_diamond": 48.5,
            "math_500": 71.3,
            "multimodal": True,
            "agentic_tasks": 55.8
        }
    }
}


class LOTModelArenaEngine:
    """
    LOT Model Arena Engine.
    Handles model selection, benchmark data serving, token counting,
    session persistence, and auto-fallback routing.
    """

    def __init__(self):
        self.registry = LOT_MODEL_REGISTRY
        self.active_model = "lot-sovereign-ultra"
        self.sessions: Dict[str, Dict[str, Any]] = {}
        logger.info("[LOTModelArenaEngine] Model Arena Engine initialized with %d models", len(self.registry))

    def get_all_models(self) -> List[Dict[str, Any]]:
        """Return all models with full metadata."""
        return [{"id": k, **v} for k, v in self.registry.items()]

    def get_benchmark_matrix(self) -> List[Dict[str, Any]]:
        """Return benchmark comparison matrix for all models."""
        matrix = []
        for model_id, model in self.registry.items():
            row = {
                "id": model_id,
                "name": model["name"],
                "context_window": model["context_window"],
                "speed": model["tokens_per_sec"],
                **model["benchmarks"]
            }
            matrix.append(row)
        return matrix

    def select_model(self, model_id: str) -> Dict[str, Any]:
        """Select active model."""
        if model_id in self.registry:
            self.active_model = model_id
            return {"status": "selected", "model": self.registry[model_id]}
        return {"status": "error", "message": f"Model '{model_id}' not found"}

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count (approx 4 chars per token)."""
        return max(1, len(text) // 4)

    def check_auto_fallback(self, current_tokens: int) -> Dict[str, Any]:
        """Check if auto-fallback should trigger based on token usage."""
        model = self.registry[self.active_model]
        max_tokens = model["context_window"]
        usage_pct = (current_tokens / max_tokens) * 100

        if usage_pct >= 80:
            return {
                "should_fallback": True,
                "fallback_model": "lot-nemotron-flash",
                "reason": f"Token usage at {usage_pct:.1f}% — auto-switching to LOT Nemotron Flash",
                "usage_percent": round(usage_pct, 1)
            }
        return {
            "should_fallback": False,
            "usage_percent": round(usage_pct, 1)
        }

    def create_session(self, title: Optional[str] = None) -> Dict[str, Any]:
        """Create a new chat session."""
        session_id = str(uuid.uuid4())[:8]
        session = {
            "id": session_id,
            "title": title or f"Session {len(self.sessions) + 1}",
            "model": self.active_model,
            "messages": [],
            "created_at": time.time(),
            "token_count": 0
        }
        self.sessions[session_id] = session
        return session

    def get_sessions(self) -> List[Dict[str, Any]]:
        """Return all sessions sorted by creation time."""
        return sorted(self.sessions.values(), key=lambda s: s["created_at"], reverse=True)

    def get_arena_status(self) -> Dict[str, Any]:
        """Return full arena status."""
        return {
            "engine": "LOT Model Arena Engine v1.0",
            "active_model": self.active_model,
            "model_count": len(self.registry),
            "session_count": len(self.sessions),
            "status": "ONLINE"
        }
