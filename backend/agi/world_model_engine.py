import ast
import json
import os
from typing import Dict, List, Set, Any

class WorldModel:
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        # edges: source_node -> target_node -> list of relation types ('calls', 'imports', 'inherits', 'uses')
        self.edges: Dict[str, Dict[str, List[str]]] = {}

    def add_node(self, node_name: str, node_type: str, metadata: Dict[str, Any] = None):
        if node_name not in self.nodes:
            self.nodes[node_name] = {'type': node_type, 'metadata': metadata or {}}

    def add_edge(self, source: str, target: str, relation: str):
        if source not in self.edges:
            self.edges[source] = {}
        if target not in self.edges[source]:
            self.edges[source][target] = []
        if relation not in self.edges[source][target]:
            self.edges[source][target].append(relation)

    def to_dict(self) -> Dict:
        return {'nodes': self.nodes, 'edges': self.edges}


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self, filename: str, module_name: str, model: WorldModel):
        self.filename = filename
        self.module_name = module_name
        self.model = model
        self.current_class = None
        self.current_function = None

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            imported_module = alias.name
            self.model.add_node(imported_module, 'module')
            self.model.add_edge(self.module_name, imported_module, 'imports')
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            self.model.add_node(node.module, 'module')
            self.model.add_edge(self.module_name, node.module, 'imports')
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        class_name = f"{self.module_name}.{node.name}"
        method_count = len([n for n in node.body if isinstance(n, ast.FunctionDef)])
        self.model.add_node(class_name, 'class', {'methods': method_count})
        
        for base in node.bases:
            if isinstance(base, ast.Name):
                self.model.add_edge(class_name, base.id, 'inherits')
                
        prev_class = self.current_class
        self.current_class = class_name
        self.generic_visit(node)
        self.current_class = prev_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        func_name = f"{self.current_class}.{node.name}" if self.current_class else f"{self.module_name}.{node.name}"
        self.model.add_node(func_name, 'function')
        
        prev_func = self.current_function
        self.current_function = func_name
        self.generic_visit(node)
        self.current_function = prev_func

    def visit_Call(self, node: ast.Call):
        if self.current_function:
            if isinstance(node.func, ast.Name):
                target = node.func.id
                self.model.add_edge(self.current_function, target, 'calls')
            elif isinstance(node.func, ast.Attribute):
                target = node.func.attr
                self.model.add_edge(self.current_function, target, 'calls')
        self.generic_visit(node)


class WorldModelEngine:
    def __init__(self):
        self.model = WorldModel()

    def build_from_directory(self, path: str) -> WorldModel:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    module_name = os.path.relpath(file_path, path).replace(os.sep, '.').replace('.py', '')
                    self.model.add_node(module_name, 'file', {'path': file_path})
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        tree = ast.parse(content)
                        analyzer = CodeAnalyzer(file_path, module_name, self.model)
                        analyzer.visit(tree)
                    except Exception as e:
                        print(f"Failed to parse {file_path}: {e}")
        
        self.save_model("default_project_hash")
        return self.model

    def get_impact_analysis(self, node_name: str) -> List[str]:
        """Predicts what breaks if node_name is removed."""
        impacted = set()
        queue = [node_name]
        
        # Traverse edges backwards
        while queue:
            current = queue.pop(0)
            for src, targets in self.model.edges.items():
                if current in targets and src not in impacted:
                    impacted.add(src)
                    queue.append(src)
        return list(impacted)

    def get_orphaned_nodes(self) -> List[str]:
        """Finds functions defined but never called."""
        called = set()
        for src, targets in self.model.edges.items():
            for target, relations in targets.items():
                if 'calls' in relations:
                    called.add(target)
                    
        orphans = []
        for name, data in self.model.nodes.items():
            if data['type'] == 'function':
                func_base = name.split('.')[-1]
                if func_base not in called and name not in called:
                    if not func_base.startswith('__'):  # Ignore magic methods
                        orphans.append(name)
        return orphans

    def get_god_classes(self) -> List[str]:
        god_classes = []
        for name, data in self.model.nodes.items():
            if data['type'] == 'class' and data.get('metadata', {}).get('methods', 0) > 20:
                god_classes.append(name)
        return god_classes

    def detect_circular_imports(self) -> List[List[str]]:
        cycles = []
        visited = set()
        
        def dfs(node, path):
            if node in path:
                cycle = path[path.index(node):]
                if sorted(cycle) not in [sorted(c) for c in cycles]:
                    cycles.append(cycle)
                return
            if node in visited:
                return
                
            visited.add(node)
            path.append(node)
            
            for target, relations in self.model.edges.get(node, {}).items():
                if 'imports' in relations:
                    dfs(target, path)
            path.pop()

        for node in self.model.nodes:
            if self.model.nodes[node]['type'] == 'module' or self.model.nodes[node]['type'] == 'file':
                dfs(node, [])
        return cycles

    def save_model(self, project_hash: str) -> None:
        save_dir = os.path.join(os.path.dirname(__file__), 'world_models')
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, f"{project_hash}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.model.to_dict(), f, indent=2)

    def to_summary(self) -> str:
        nodes_count = len(self.model.nodes)
        edges_count = sum(len(targets) for targets in self.model.edges.values())
        return f"World Model Summary: {nodes_count} nodes, {edges_count} edges."


def inject_world_model_prompt(system_prompt: str, task: str) -> str:
    injection = (
        "\\n[WORLD MODEL CONTEXT]\\n"
        "Consider the global impact of your changes.\\n"
        "Avoid creating orphaned functions or god classes.\\n"
        "Ensure no circular dependencies are introduced.\\n"
    )
    return system_prompt + injection
