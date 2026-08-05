import json
import ast
import os
import time
from typing import Dict, List, Any

class SEALRewardFunctions:
    def __init__(self, log_path: str = 'backend/asi/seal_rewards_log.json'):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                json.dump([], f)

    def code_correctness_reward(self, code: str, test_results: Dict) -> float:
        pass_rate = test_results.get('pass_rate', 0.0)
        syntax_errors = 1 if test_results.get('syntax_errors', False) else 0
        runtime_errors = 1 if test_results.get('runtime_errors', False) else 0
        
        score = (pass_rate * 0.7) + ((1 - syntax_errors) * 0.2) + ((1 - runtime_errors) * 0.1)
        return max(0.0, min(1.0, score))

    def code_quality_reward(self, code: str) -> float:
        try:
            tree = ast.parse(code)
            complexity_penalty = min(0.5, len(list(ast.walk(tree))) / 1000.0)
        except:
            complexity_penalty = 1.0
        
        security_score = 1.0
        if 'eval(' in code or 'exec(' in code:
            security_score = 0.0
            
        style_score = 1.0
        score = ((1.0 - complexity_penalty) * 0.4) + (security_score * 0.3) + (style_score * 0.3)
        return max(0.0, min(1.0, score))

    def architecture_coherence_reward(self, task: str, output: str) -> float:
        task_relevance = 1.0 if task.lower() in output.lower() else 0.5
        completeness = 0.8
        no_hallucinations = 1.0 if 'TODO' not in output else 0.5
        score = (task_relevance * 0.4) + (completeness * 0.3) + (no_hallucinations * 0.3)
        return max(0.0, min(1.0, score))

    def composite_reward(self, code: str, test_results: Dict, task: str, output: str) -> Dict[str, float]:
        r_corr = self.code_correctness_reward(code, test_results)
        r_qual = self.code_quality_reward(code)
        r_coh = self.architecture_coherence_reward(task, output)
        total = (0.5 * r_corr) + (0.3 * r_qual) + (0.2 * r_coh)
        return {
            'total': total,
            'correctness': r_corr,
            'quality': r_qual,
            'coherence': r_coh
        }

    def anti_rationalization_reward(self, output: str) -> float:
        penalties = ['TODO', 'placeholder', 'implement later', 'stub', 'pass # fix later', '...']
        num_rationalizations = sum(1 for p in penalties if p.lower() in output.lower())
        score = 1.0 - (num_rationalizations * 0.1)
        return max(0.0, min(1.0, score))

    def evidence_gate_reward(self, output: str, required_evidence: List[str]) -> float:
        if not required_evidence:
            return 1.0
        found = sum(1 for ev in required_evidence if ev in output)
        return found / len(required_evidence)

    def get_reward_history(self) -> List[Dict]:
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as f:
                return json.load(f)
        return []

    def store_reward(self, task_id: str, rewards: Dict) -> None:
        history = self.get_reward_history()
        history.append({'task_id': task_id, 'timestamp': time.time(), 'rewards': rewards})
        with open(self.log_path, 'w') as f:
            json.dump(history, f, indent=2)

def inject_seal_rewards_prompt(system_prompt: str) -> str:
    return system_prompt + "\n[SYSTEM INJECT] SEAL Rewards tracking active. Outputs are evaluated for correctness, quality, coherence, and lack of rationalization."
