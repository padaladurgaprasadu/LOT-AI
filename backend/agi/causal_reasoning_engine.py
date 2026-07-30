import json
import re
from typing import Dict, List, Set, Optional, Tuple

class CausalGraph:
    """Represents a causal graph using adjacency lists."""
    def __init__(self):
        # Maps effect to a list of its causes: {effect_node: [cause_nodes]}
        self.edges: Dict[str, List[str]] = {}
        self.nodes: Set[str] = set()

    def add_node(self, node: str) -> None:
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = []

    def add_edge(self, cause: str, effect: str, relation: str = "causes") -> None:
        self.add_node(cause)
        self.add_node(effect)
        if cause not in self.edges[effect]:
            self.edges[effect].append(cause)

    def get_root_causes(self) -> List[str]:
        """Nodes with no causes (in-degree 0 in the context of cause->effect)."""
        roots = []
        for node in self.nodes:
            # If node is never an effect, it's a root cause
            if not self.edges.get(node):
                roots.append(node)
        return roots

    def get_downstream_effects(self, node: str) -> List[str]:
        """Finds all nodes that are caused by this node (directly or indirectly)."""
        effects = set()
        queue = [node]
        while queue:
            current = queue.pop(0)
            for effect, causes in self.edges.items():
                if current in causes and effect not in effects:
                    effects.add(effect)
                    queue.append(effect)
        return list(effects)

    def is_cyclic(self) -> bool:
        """Detects if there are causal cycles."""
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            
            # Find all nodes that this node causes
            for effect, causes in self.edges.items():
                if node in causes:
                    if effect not in visited:
                        if dfs(effect):
                            return True
                    elif effect in rec_stack:
                        return True
            rec_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited:
                if dfs(node):
                    return True
        return False

    def get_intervention_points(self) -> List[str]:
        """Identifies critical dependencies (nodes with high out-degree)."""
        out_degrees: Dict[str, int] = {node: 0 for node in self.nodes}
        for effect, causes in self.edges.items():
            for cause in causes:
                out_degrees[cause] += 1
        
        # Return sorted by highest out-degree
        sorted_nodes = sorted(out_degrees.items(), key=lambda item: item[1], reverse=True)
        return [node for node, count in sorted_nodes if count > 0]


class CausalReasoningEngine:
    """Engine for building and querying causal graphs using Pearl's do-calculus principles."""
    
    def analyze_description(self, text: str) -> CausalGraph:
        """Builds causal chains from natural language descriptions."""
        graph = CausalGraph()
        
        # Simplified keyword extraction for demonstration
        sentences = re.split(r'[.!?]', text)
        causal_keywords = [' causes ', ' leads to ', ' results in ', ' triggers ', ' forces ']
        
        for sentence in sentences:
            sentence = sentence.strip().lower()
            if not sentence:
                continue
            
            for keyword in causal_keywords:
                if keyword in sentence:
                    parts = sentence.split(keyword)
                    if len(parts) == 2:
                        cause, effect = parts[0].strip(), parts[1].strip()
                        graph.add_edge(cause, effect)
                        break
        
        return graph

    def explain_bug(self, error: str, context: str) -> str:
        """Traces error back through causal chain to root cause."""
        graph = self.analyze_description(context)
        graph.add_node(error)
        
        if graph.is_cyclic():
            return "Analysis failed: The causal description contains circular dependencies (architectural anti-pattern)."
            
        roots = graph.get_root_causes()
        if not roots:
            return "Could not determine the root cause from the provided context."
            
        return f"The root cause of the error '{error}' is likely: {', '.join(roots)}. Intervening on these points will prevent the downstream failure."


def inject_causal_reasoning_prompt(system_prompt: str) -> str:
    """Injects causal reasoning guidelines into the system prompt."""
    causal_instructions = (
        "\\n[CAUSAL REASONING REQUIRED]\\n"
        "Apply Pearl's do-calculus principles:\\n"
        "1. Identify causal chains and intervention points.\\n"
        "2. Avoid confusing correlation with causation.\\n"
        "3. Evaluate counterfactuals ('what if X was removed?').\\n"
        "4. Detect and warn against circular dependencies.\\n"
    )
    return system_prompt + causal_instructions
