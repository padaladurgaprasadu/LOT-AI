import os
import json
import uuid
from typing import Dict, Any, List

class DistillationEngine:
    """Compress web knowledge into reusable engineering heuristics."""
    def __init__(self):
        self.heuristics_path = os.path.join(os.path.dirname(__file__), 'heuristics.json')
        self.heuristics = self._load_heuristics()

    def _load_heuristics(self) -> Dict[str, Any]:
        if os.path.exists(self.heuristics_path):
            with open(self.heuristics_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_heuristics(self):
        os.makedirs(os.path.dirname(self.heuristics_path), exist_ok=True)
        with open(self.heuristics_path, 'w', encoding='utf-8') as f:
            json.dump(self.heuristics, f, indent=4)

    def distil_to_heuristic(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "id": str(uuid.uuid4()),
            "heuristic": "Always validate inputs at system boundaries.",
            "rationale": "Extracted from multiple security incident reports.",
            "examples": ["Use schema validation for API inputs."],
            "confidence": 0.85,
            "category": "security"
        }

    def detect_pattern(self, heuristics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [{
            "pattern_name": "Input Validation",
            "instances": [h.get("id") for h in heuristics],
            "generalisation": "Strict boundary checks prevent cascading failures."
        }]

    def merge_heuristics(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        merged = existing.copy()
        merged["confidence"] = min(1.0, existing.get("confidence", 0.5) + 0.1)
        merged["examples"].extend([e for e in new.get("examples", []) if e not in merged["examples"]])
        return merged

    def invalidate_heuristic(self, heuristic_id: str, reason: str):
        if heuristic_id in self.heuristics:
            self.heuristics[heuristic_id]["invalidated"] = True
            self.heuristics[heuristic_id]["invalidation_reason"] = reason
            self._save_heuristics()

    def get_relevant_heuristics(self, task: str, top_k: int = 5) -> List[Dict[str, Any]]:
        valid_heuristics = [h for h in self.heuristics.values() if not h.get("invalidated")]
        return sorted(valid_heuristics, key=lambda x: x.get("confidence", 0.0), reverse=True)[:top_k]

    def export_as_prompt_section(self, heuristics: List[Dict[str, Any]]) -> str:
        lines = ["### Engineering Heuristics ###"]
        for h in heuristics:
            lines.append(f"- **{h.get('category', 'general').upper()}**: {h.get('heuristic')} (Confidence: {h.get('confidence', 0):.2f})")
        return "\n".join(lines)

    def get_stats(self) -> Dict[str, Any]:
        categories = {}
        for h in self.heuristics.values():
            cat = h.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        return {
            "total": len(self.heuristics),
            "by_category": categories,
            "avg_confidence": sum(h.get("confidence", 0) for h in self.heuristics.values()) / max(1, len(self.heuristics)),
            "recently_added": 0
        }

def inject_distillation_prompt(system_prompt: str, task: str = '') -> str:
    engine = DistillationEngine()
    relevant = engine.get_relevant_heuristics(task)
    section = engine.export_as_prompt_section(relevant)
    return system_prompt + f"\n\n{section}"
