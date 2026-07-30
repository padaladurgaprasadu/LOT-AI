from typing import List, Dict, Optional
import json

class Analogy:
    def __init__(self, source_domain: str, source_pattern: str, target_domain: str, target_pattern: str, explanation: str, use_when: List[str]):
        self.source_domain = source_domain
        self.source_pattern = source_pattern
        self.target_domain = target_domain
        self.target_pattern = target_pattern
        self.explanation = explanation
        self.use_when = use_when

    def to_dict(self) -> Dict:
        return {
            "source_domain": self.source_domain,
            "source_pattern": self.source_pattern,
            "target_domain": self.target_domain,
            "target_pattern": self.target_pattern,
            "explanation": self.explanation,
            "use_when": self.use_when
        }


class TransferLearningEngine:
    def __init__(self):
        self.analogies: List[Analogy] = self._load_default_analogies()

    def _load_default_analogies(self) -> List[Analogy]:
        # Minimal set for example
        return [
            Analogy("Erlang", "Actor Model", "Python", "asyncio event loop", "Concurrency isolation model.", ["concurrency", "isolation"]),
            Analogy("Distributed Systems", "Circuit Breaker", "React", "Error Boundary", "Failing gracefully.", ["error handling", "resilience"]),
            Analogy("Algorithms", "Memoization", "React", "useMemo / Redis caching", "Cache results for reuse.", ["performance", "caching"]),
            Analogy("Distributed Systems", "Raft consensus", "UI", "optimistic updates with conflict resolution", "State synchronization.", ["sync", "state"]),
            Analogy("Geometry", "Bézier curves", "CSS", "cubic-bezier animations", "Smooth transitions.", ["animation", "easing"]),
            Analogy("Networking", "TCP backpressure", "API", "rate limiting", "Preventing overload.", ["overload", "throttling"]),
            Analogy("Big Data", "MapReduce", "Testing", "parallel test execution", "Divide and conquer.", ["parallel", "speedup"]),
            Analogy("Data Structures", "Bloom filter", "Feature Flags", "A/B testing", "Probabilistic membership check.", ["testing", "flags"]),
            Analogy("Architecture", "CQRS", "State Management", "Redux command/query separation", "Segregate read/write.", ["state", "architecture"]),
            Analogy("Distributed Transactions", "Saga pattern", "UI", "multi-step form wizard", "Long running transaction.", ["wizard", "transaction"])
        ]

    def search_analogies(self, problem: str, top_k: int = 3) -> List[Analogy]:
        problem = problem.lower()
        scored = []
        for analogy in self.analogies:
            score = 0
            for term in analogy.use_when:
                if term.lower() in problem:
                    score += 1
            if analogy.target_domain.lower() in problem or analogy.source_domain.lower() in problem:
                score += 1
            scored.append((score, analogy))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [a for s, a in scored[:top_k] if s > 0] or [a for s, a in scored[:top_k]]

    def get_analogy_for_domains(self, source: str, target: str) -> Optional[Analogy]:
        for analogy in self.analogies:
            if analogy.source_domain.lower() == source.lower() and analogy.target_domain.lower() == target.lower():
                return analogy
        return None

def inject_transfer_learning_prompt(system_prompt: str, task: str) -> str:
    return system_prompt + "\\n[TRANSFER LEARNING] Use cross-domain analogies to solve this task.\\n"
