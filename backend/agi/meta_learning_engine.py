import json
import os
from typing import List, Dict, Any

class MetaLearningEngine:
    def __init__(self):
        self.concepts: Dict[str, Dict[str, Any]] = {}
        self.storage_path = os.path.join(os.path.dirname(__file__), 'learned_concepts.json')
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                self.concepts = json.load(f)

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.concepts, f, indent=2)

    def learn_concept(self, name: str, examples: List[str], domain: str):
        times_seen = len(examples)
        confidence = min(1.0, 0.6 + (times_seen - 1) * 0.04) # grows to ~1.0 at 10 examples
        
        # Mock bootstrap using transfer learning logic
        if domain in ["Transferable"]:
            confidence = max(confidence, 0.8)

        self.concepts[name] = {
            "name": name,
            "domain": domain,
            "examples": examples,
            "generalisation": f"Generalized rule for {name}",
            "confidence": confidence,
            "times_seen": times_seen
        }
        self._save()

    def apply_concept(self, name: str, new_context: str) -> str:
        if name in self.concepts:
            return f"Applying {name} to {new_context} based on {self.concepts[name]['generalisation']}"
        return f"Concept {name} not found."

    def get_confidence(self, name: str) -> float:
        return self.concepts.get(name, {}).get("confidence", 0.0)

    def get_stats(self) -> Dict:
        return {
            "total_concepts": len(self.concepts),
            "average_confidence": sum(c["confidence"] for c in self.concepts.values()) / max(1, len(self.concepts))
        }

def inject_meta_learning_prompt(system_prompt: str, task: str) -> str:
    return system_prompt + "\\n[META LEARNING] Use past concept generalizations to accelerate task completion.\\n"
