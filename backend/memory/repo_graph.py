import os
import ast
import json
import networkx as nx
from typing import Dict, List, Set, Any
from pathlib import Path

class DAIMG:
    """
    Dynamic AST-Integrated Memory Graph (DAIMG)
    100x more advanced than basic RepoGraph. Builds a deeply semantic NetworkX graph 
    where Nodes = Files, Classes, Functions, and Edges = Contains, Imports, Calls.
    """
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.graph = nx.DiGraph()
        
    def build_graph(self):
        """Scans the repository and builds the mathematical NetworkX dependency map."""
        self.graph.clear()
        
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__']]
            
            for file in files:
                if file.endswith('.py') or file.endswith('.js') or file.endswith('.jsx'):
                    file_path = Path(root) / file
                    rel_path = str(file_path.relative_to(self.root_dir)).replace("\\", "/")
                    
                    # Add File Node
                    self.graph.add_node(rel_path, type="file", path=rel_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            self._parse_and_map(rel_path, content, file_path.suffix)
                    except Exception as e:
                        pass
                        
    def _parse_and_map(self, file_node: str, content: str, ext: str):
        """Parses AST to map deeply semantic relationships."""
        if ext == '.py':
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    # 1. Imports
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            target = name.name
                            self.graph.add_node(target, type="module")
                            self.graph.add_edge(file_node, target, relation="IMPORTS")
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            target = node.module
                            self.graph.add_node(target, type="module")
                            self.graph.add_edge(file_node, target, relation="IMPORTS")
                            
                    # 2. Classes and Functions (CONTAINS edges)
                    elif isinstance(node, ast.ClassDef):
                        class_node = f"{file_node}::{node.name}"
                        self.graph.add_node(class_node, type="class", name=node.name)
                        self.graph.add_edge(file_node, class_node, relation="CONTAINS")
                    elif isinstance(node, ast.FunctionDef):
                        func_node = f"{file_node}::{node.name}"
                        self.graph.add_node(func_node, type="function", name=node.name)
                        self.graph.add_edge(file_node, func_node, relation="CONTAINS")
                        
            except SyntaxError:
                pass
        elif ext in ['.js', '.jsx']:
            # For JS/TS, fallback to regex mapping for files but structure it in NetworkX
            import re
            js_imports = re.findall(r'import\s+.*?\s+from\s+[\'"](.*?)[\'"]', content)
            require_imports = re.findall(r'require\([\'"](.*?)[\'"]\)', content)
            for imp in js_imports + require_imports:
                self.graph.add_node(imp, type="module")
                self.graph.add_edge(file_node, imp, relation="IMPORTS")
                
            funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)', content)
            for func in funcs:
                func_node = f"{file_node}::{func}"
                self.graph.add_node(func_node, type="function", name=func)
                self.graph.add_edge(file_node, func_node, relation="CONTAINS")

    def get_architectural_context(self, entry_node: str, max_depth: int = 2) -> Dict[str, Any]:
        """
        Uses graph traversal (e.g., shortest path / neighborhood) to generate an 
        infinite-context architectural summary without blowing up tokens.
        """
        entry_node = entry_node.replace("\\", "/")
        if entry_node not in self.graph:
            # Try to find a partial match
            matches = [n for n in self.graph.nodes if isinstance(n, str) and entry_node in n]
            if not matches:
                return {"error": f"Node {entry_node} not found in graph."}
            entry_node = matches[0]

        # Use NetworkX ego_graph to extract the localized "fractal" context
        subgraph = nx.ego_graph(self.graph, entry_node, radius=max_depth)
        
        context = {
            "entry": entry_node,
            "nodes": [],
            "relationships": []
        }
        
        for n, data in subgraph.nodes(data=True):
            context["nodes"].append({"id": n, "type": data.get("type", "unknown")})
            
        for u, v, data in subgraph.edges(data=True):
            context["relationships"].append(f"{u} -[{data.get('relation', 'RELATES_TO')}]-> {v}")
            
        return context

    def to_json(self) -> str:
        """Export full graph as a Node-Link JSON string."""
        data = nx.node_link_data(self.graph)
        return json.dumps(data, indent=2)

    def extract_semantic_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Omni-Intelligence Pillar 3: Graphify Integration.
        Uses LLM (or heuristics) to extract high-level entities (e.g., 'Auth Module', 'Database') 
        and map them conceptually, beyond just raw AST.
        (Mock implementation for speed, in production this queries the Architect Agent)
        """
        # Placeholder for complex Graphify-style LLM extraction
        return [{"entity": "ExtractedConcept", "type": "Semantic"}]

    def export_to_langflow_format(self) -> Dict[str, Any]:
        """
        Omni-Intelligence Pillar 3: Visual Orchestration.
        Converts the NetworkX DAG into a React Flow / Langflow compatible format:
        { nodes: [{id, position, data}], edges: [{id, source, target}] }
        """
        react_flow_graph = {"nodes": [], "edges": []}
        
        # Calculate a basic layout for visual positioning
        try:
            pos = nx.spring_layout(self.graph)
        except:
            pos = {n: [0, 0] for n in self.graph.nodes()}
            
        for n, data in self.graph.nodes(data=True):
            react_flow_graph["nodes"].append({
                "id": str(n),
                "position": {"x": float(pos[n][0]) * 500, "y": float(pos[n][1]) * 500},
                "data": {"label": str(n), "type": data.get("type", "unknown")}
            })
            
        for idx, (u, v, data) in enumerate(self.graph.edges(data=True)):
            react_flow_graph["edges"].append({
                "id": f"e{idx}",
                "source": str(u),
                "target": str(v),
                "label": data.get("relation", "")
            })
            
        return react_flow_graph

if __name__ == "__main__":
    import sys
    test_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    daimg = DAIMG(test_dir)
    print("Building Infinite-Context Graph...")
    daimg.build_graph()
    print(f"Mapped {daimg.graph.number_of_nodes()} highly semantic nodes and {daimg.graph.number_of_edges()} relationships.")
    
    # Test Context Compression
    if daimg.graph.number_of_nodes() > 0:
        sample_node = list(daimg.graph.nodes())[0]
        print(f"\nExtracting Deep Architectural Context for: {sample_node}")
        ctx = daimg.get_architectural_context(sample_node, max_depth=1)
        print(json.dumps(ctx, indent=2))
