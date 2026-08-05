import json
import os
import hashlib
from dataclasses import dataclass, asdict
from typing import Dict, List, Any

@dataclass
class TrainingExample:
    instruction: str
    input_text: str
    output_text: str
    domain: str
    quality_score: float
    bloom_level: int
    reward_score: float
    source: str

class DatasetCurator:
    def curate_from_event_stream(self, event_stream_path: str = 'backend/asi/event_stream_log.jsonl') -> List[TrainingExample]:
        examples = []
        if not os.path.exists(event_stream_path):
            return examples
            
        with open(event_stream_path, 'r') as f:
            for line in f:
                try:
                    evt = json.loads(line)
                    if evt.get('event_type') == 'SEALAdaptationEvent' and evt.get('top_reward', 0) >= 0.85:
                        ex = TrainingExample(
                            instruction="Adapt to SEAL environment",
                            input_text=str(evt.get('candidates_generated', '')),
                            output_text=f"Accepted edits: {evt.get('edits_accepted')}",
                            domain="agentic_adaptation",
                            quality_score=evt.get('top_reward', 0),
                            bloom_level=4,
                            reward_score=evt.get('top_reward', 0),
                            source="event_stream"
                        )
                        examples.append(ex)
                except Exception:
                    pass
        return examples

    def curate_from_conversations(self, conversations_dir: str) -> List[TrainingExample]:
        return []

    def score_quality(self, example: TrainingExample) -> float:
        code_correctness = example.reward_score
        complexity = 0.5
        completeness = 0.9
        style = 0.8
        score = (code_correctness * 0.3) + (complexity * 0.2) + (completeness * 0.3) + (style * 0.2)
        return min(1.0, max(0.0, score))

    def deduplicate(self, examples: List[TrainingExample], similarity_threshold: float = 0.85) -> List[TrainingExample]:
        seen_hashes = set()
        unique = []
        for ex in examples:
            h = hashlib.md5(ex.instruction.encode('utf-8')).hexdigest()
            if h not in seen_hashes:
                seen_hashes.add(h)
                unique.append(ex)
        return unique

    def balance_domains(self, examples: List[TrainingExample], max_per_domain: int = 5000) -> List[TrainingExample]:
        domain_counts = {}
        balanced = []
        for ex in examples:
            domain = ex.domain
            if domain_counts.get(domain, 0) < max_per_domain:
                balanced.append(ex)
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
        return balanced

    def generate_dpo_pairs(self, examples: List[TrainingExample]) -> List[Dict[str, str]]:
        pairs = []
        for ex in examples:
            pairs.append({
                'prompt': f"{ex.instruction}\n{ex.input_text}",
                'chosen': ex.output_text,
                'rejected': ex.output_text[:len(ex.output_text)//2] + " [TRUNCATED] "
            })
        return pairs

    def export_to_jsonl(self, examples: List[TrainingExample], output_path: str) -> int:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        count = 0
        with open(output_path, 'w') as f:
            for ex in examples:
                f.write(json.dumps(asdict(ex)) + '\n')
                count += 1
        return count

    def get_stats(self) -> Dict[str, Any]:
        return {
            'total': 0,
            'by_domain': {},
            'avg_quality': 0.0,
            'avg_reward': 0.0,
            'bloom_distribution': {}
        }

def inject_curator_prompt(system_prompt: str) -> str:
    return system_prompt + "\n[SYSTEM INJECT] Dataset curator active. Quality filtering based on bloom levels and SEAL rewards."
