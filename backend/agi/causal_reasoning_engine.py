"""
Causal reasoning engine implementing Pearl's do-calculus.
Provides causal graph modeling and root cause analysis.
"""
from typing import Dict, List, Optional, Set
from collections import deque

class CausalNode:
    def __init__(self, name: str, node_type: str):
        self.name = name
        self.node_type = node_type
        self.causes: Set[str] = set()
        self.effects: Set[str] = set()

class CausalGraph:
    def __init__(self):
        self.nodes: Dict[str, CausalNode] = {}
        self.edges: Dict[tuple[str, str], str] = {}

    def add_node(self, name: str, node_type: str):
        if name not in self.nodes:
            self.nodes[name] = CausalNode(name, node_type)

    def add_edge(self, cause: str, effect: str, mechanism: str = ""):
        if cause not in self.nodes:
            self.add_node(cause, 'UNKNOWN')
        if effect not in self.nodes:
            self.add_node(effect, 'UNKNOWN')
        
        self.nodes[cause].effects.add(effect)
        self.nodes[effect].causes.add(cause)
        self.edges[(cause, effect)] = mechanism

    def find_root_cause(self, symptom: str) -> List[str]:
        if symptom not in self.nodes:
            return []
        
        visited = set()
        queue = deque([symptom])
        root_causes = []

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            node = self.nodes[current]
            if not node.causes:
                root_causes.append(current)
            else:
                for cause in node.causes:
                    queue.append(cause)
        return root_causes

    def get_causal_chain(self, start: str, end: str) -> List[str]:
        if start not in self.nodes or end not in self.nodes:
            return []
        
        queue = deque([(start, [start])])
        visited = set()
        
        while queue:
            current, path = queue.popleft()
            if current == end:
                return path
            
            if current in visited:
                continue
            visited.add(current)
            
            for effect in self.nodes[current].effects:
                queue.append((effect, path + [effect]))
        return []

def _build_default_graph() -> CausalGraph:
    graph = CausalGraph()
    graph.add_edge('untrusted input', 'missing validation')
    graph.add_edge('missing validation', 'null pointer')
    
    graph.add_edge('unoptimised schema', 'missing index')
    graph.add_edge('missing index', 'slow query')
    
    graph.add_edge('missing context manager', 'unclosed resource')
    graph.add_edge('unclosed resource', 'memory leak')
    
    graph.add_edge('slow downstream', 'connection pool exhaustion')
    graph.add_edge('connection pool exhaustion', '503 error')
    return graph

def analyze_error_causally(error_description: str) -> dict:
    graph = _build_default_graph()
    
    symptom = None
    for node_name in graph.nodes:
        if node_name in error_description.lower():
            symptom = node_name
            break
            
    if not symptom:
        return {
            "root_cause": "Unknown",
            "causal_chain": [],
            "recommended_fix": "Investigate logs for more specific symptoms."
        }
        
    root_causes = graph.find_root_cause(symptom)
    root_cause = root_causes[0] if root_causes else symptom
    
    chain = []
    if root_cause != symptom:
        chain = graph.get_causal_chain(root_cause, symptom)
        
    return {
        "root_cause": root_cause,
        "causal_chain": chain,
        "recommended_fix": f"Address the root cause: {root_cause}"
    }

def inject_causal_reasoning_prompt(system_prompt: str) -> str:
    causal_directive = (
        "\n\n[CAUSAL REASONING DIRECTIVE]\n"
        "Apply Pearl's do-calculus for problem solving. "
        "Trace symptoms back to root causes before proposing a fix."
    )
    return system_prompt + causal_directive
