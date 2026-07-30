"""
Few-shot learning accelerator and learning strategy optimiser.
Extracts patterns from examples and tracks user learning velocity.
"""
from typing import List, Dict, Any

class FewShotLearner:
    def __init__(self):
        self.examples: List[Dict[str, Any]] = []
        
    def add_example(self, context: str, input_data: str, output_data: str):
        self.examples.append({
            "context": context,
            "input": input_data,
            "output": output_data
        })
        
    def predict(self, new_input: str) -> str:
        if not self.examples:
            return "No examples to learn from."
        return f"Predicted based on '{self.examples[0]['input']}': {self.examples[0]['output']}"

class LearningVelocityTracker:
    def __init__(self):
        self.sessions: Dict[str, List[bool]] = {}
        
    def track_session(self, user_id: str, concept: str, understood: bool):
        if user_id not in self.sessions:
            self.sessions[user_id] = []
        self.sessions[user_id].append(understood)
        
    def get_velocity(self, user_id: str) -> float:
        if user_id not in self.sessions or not self.sessions[user_id]:
            return 0.0
        history = self.sessions[user_id]
        return sum(history) / len(history)

def bootstrap_library_knowledge(examples: List[str], library_name: str) -> dict:
    patterns = []
    if any("import" in ex for ex in examples):
        patterns.append("Standard import pattern detected")
        
    return {
        "library_name": library_name,
        "api_patterns": patterns,
        "common_idioms": ["Initialization before use", "Error catching block"],
        "gotchas": ["Watch out for async resolution", "Check null values"]
    }

def get_optimal_explanation_strategy(user_level: str, concept: str) -> str:
    if user_level.lower() == 'beginner':
        return f"Explain {concept} using analogies and avoid jargon."
    elif user_level.lower() == 'intermediate':
        return f"Explain {concept} with code examples and standard patterns."
    else:
        return f"Explain {concept} diving deep into internals, performance, and edge cases."

def inject_meta_learning_prompt(system_prompt: str) -> str:
    directive = (
        "\n\n[META LEARNING DIRECTIVE]\n"
        "Adapt your response based on few-shot examples and user learning velocity."
    )
    return system_prompt + directive
