import os
import json
import uuid
import ast
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ImprovementSuggestion:
    file_path: str
    function_name: str
    issue_type: str
    description: str
    priority: int
    suggested_fix: str
    
    def to_dict(self):
        return {
            'file_path': self.file_path,
            'function_name': self.function_name,
            'issue_type': self.issue_type,
            'description': self.description,
            'priority': self.priority,
            'suggested_fix': self.suggested_fix
        }

class RecursiveImprovementEngine:
    def __init__(self, queue_file: str = 'backend/asi/improvement_queue.json'):
        self.queue_file = queue_file
        if not os.path.exists(os.path.dirname(self.queue_file)):
            os.makedirs(os.path.dirname(self.queue_file), exist_ok=True)
        if not os.path.exists(self.queue_file):
            with open(self.queue_file, 'w') as f:
                json.dump([], f)
                
    def scan_codebase(self, base_path: str) -> List[ImprovementSuggestion]:
        suggestions = []
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.splitlines()
                        
                        # Rule 1: File length > 300 lines
                        if len(lines) > 300:
                            suggestions.append(ImprovementSuggestion(
                                file_path=full_path, function_name="global",
                                issue_type="file_length", description="File exceeds 300 lines",
                                priority=3, suggested_fix="Refactor into smaller modules"
                            ))
                            
                        # Rule 5: TODO/FIXME/HACK comments
                        for i, line in enumerate(lines):
                            lower_line = line.lower()
                            if 'todo' in lower_line or 'fixme' in lower_line or 'hack' in lower_line:
                                suggestions.append(ImprovementSuggestion(
                                    file_path=full_path, function_name="global",
                                    issue_type="tech_debt", description=f"Found tech debt comment on line {i+1}",
                                    priority=2, suggested_fix="Resolve the TODO/FIXME/HACK comment"
                                ))
                                
                        try:
                            tree = ast.parse(content)
                            for node in ast.walk(tree):
                                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                    # Rule 3: Missing docstrings
                                    if not ast.get_docstring(node):
                                        suggestions.append(ImprovementSuggestion(
                                            file_path=full_path, function_name=node.name,
                                            issue_type="missing_docstring", description="Function missing docstring",
                                            priority=1, suggested_fix="Add docstring explaining function behavior"
                                        ))
                                        
                                    # Rule 2: Cyclomatic complexity > 10
                                    complexity = sum(1 for n in ast.walk(node) if isinstance(n, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.BoolOp)))
                                    if complexity > 10:
                                        suggestions.append(ImprovementSuggestion(
                                            file_path=full_path, function_name=node.name,
                                            issue_type="high_complexity", description=f"Cyclomatic complexity {complexity} > 10",
                                            priority=4, suggested_fix="Refactor function to reduce complexity"
                                        ))
                                        
                                    # Rule 6: Functions longer than 50 lines
                                    if hasattr(node, 'end_lineno') and hasattr(node, 'lineno') and node.end_lineno - node.lineno > 50:
                                        suggestions.append(ImprovementSuggestion(
                                            file_path=full_path, function_name=node.name,
                                            issue_type="function_length", description="Function exceeds 50 lines",
                                            priority=3, suggested_fix="Extract sub-functions"
                                        ))
                                        
                                # Rule 4: Bare except clauses
                                if isinstance(node, ast.ExceptHandler):
                                    if node.type is None or (isinstance(node.type, ast.Name) and node.type.id == 'Exception'):
                                        suggestions.append(ImprovementSuggestion(
                                            file_path=full_path, function_name="global",
                                            issue_type="bare_except", description="Bare except clause used",
                                            priority=4, suggested_fix="Catch specific exceptions"
                                        ))
                        except SyntaxError:
                            pass
        return suggestions
        
    def add_to_queue(self, suggestion: ImprovementSuggestion) -> str:
        queue = self.get_queue()
        queue_id = str(uuid.uuid4())
        item = suggestion.to_dict()
        item['queue_id'] = queue_id
        item['approved'] = False
        queue.append(item)
        
        with open(self.queue_file, 'w') as f:
            json.dump(queue, f, indent=4)
            
        return queue_id
        
    def get_queue(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.queue_file):
            return []
        with open(self.queue_file, 'r') as f:
            return json.load(f)
            
    def approve_suggestion(self, queue_id: str) -> bool:
        queue = self.get_queue()
        found = False
        for item in queue:
            if item.get('queue_id') == queue_id:
                item['approved'] = True
                found = True
                break
        if found:
            with open(self.queue_file, 'w') as f:
                json.dump(queue, f, indent=4)
        return found

    def execute_approved_improvements(self) -> List[Dict[str, Any]]:
        queue = self.get_queue()
        executed = []
        for item in queue:
            if item.get('approved') and not item.get('executed'):
                item['executed'] = True
                executed.append(item)
        if executed:
            with open(self.queue_file, 'w') as f:
                json.dump(queue, f, indent=4)
        return executed

    def get_improvement_stats(self) -> Dict[str, int]:
        queue = self.get_queue()
        total = len(queue)
        approved = sum(1 for item in queue if item.get('approved'))
        executed = sum(1 for item in queue if item.get('executed'))
        pending = total - executed
        return {
            'total': total,
            'approved': approved,
            'executed': executed,
            'pending': pending
        }
