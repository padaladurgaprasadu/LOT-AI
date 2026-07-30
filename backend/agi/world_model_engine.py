"""
Live semantic codebase knowledge graph.
Builds and queries relationships between files, classes, and functions.
"""
import json
import re
from typing import Dict, List, Set, Any

class WorldModel:
    def __init__(self):
        self.files: Dict[str, str] = {}
        self.functions: Dict[str, Dict[str, Any]] = {}
        self.classes: Dict[str, Dict[str, Any]] = {}
        self.dependencies: Dict[str, str] = {}
        
    def add_file(self, path: str, content: str):
        self.files[path] = content
        
    def add_function(self, name: str, file: str, calls: List[str], lines: int):
        self.functions[name] = {
            "file": file,
            "calls": calls,
            "lines": lines
        }
        
    def add_class(self, name: str, file: str, methods: List[str], inherits: List[str]):
        self.classes[name] = {
            "file": file,
            "methods": methods,
            "inherits": inherits
        }
        
    def add_dependency(self, module: str, version: str):
        self.dependencies[module] = version
        
    def find_callers(self, function_name: str) -> List[str]:
        callers = []
        for func, data in self.functions.items():
            if function_name in data["calls"]:
                callers.append(func)
        return callers
        
    def find_dependencies(self, module: str) -> List[str]:
        return [dep for dep in self.dependencies if module in dep]
        
    def get_impact_of_change(self, element: str) -> List[str]:
        impacted = set()
        queue = [element]
        
        while queue:
            curr = queue.pop(0)
            if curr in impacted:
                continue
            impacted.add(curr)
            
            callers = self.find_callers(curr)
            queue.extend([c for c in callers if c not in impacted])
            
            for cls_name, cls_data in self.classes.items():
                if curr in cls_data["inherits"]:
                    queue.append(cls_name)
                    
        return list(impacted - {element})
        
    def find_orphans(self) -> List[str]:
        orphans = []
        for func in self.functions:
            if not self.find_callers(func):
                orphans.append(func)
        return orphans
        
    def to_json(self) -> str:
        return json.dumps({
            "files": self.files,
            "functions": self.functions,
            "classes": self.classes,
            "dependencies": self.dependencies
        })

def build_from_code(code: str, filename: str = 'main.py') -> WorldModel:
    model = WorldModel()
    model.add_file(filename, code)
    
    imports = re.findall(r'^import (\w+)', code, re.MULTILINE)
    for imp in imports:
        model.add_dependency(imp, "latest")
        
    functions = re.findall(r'def (\w+)\(', code)
    for func in functions:
        model.add_function(func, filename, [], 10)
        
    classes = re.findall(r'class (\w+)', code)
    for cls in classes:
        model.add_class(cls, filename, [], [])
        
    return model

def inject_world_model_prompt(system_prompt: str, model_summary: str = '') -> str:
    directive = (
        f"\n\n[WORLD MODEL DIRECTIVE]\n"
        f"Consider the entire codebase impact. Current model summary: {model_summary}"
    )
    return system_prompt + directive
