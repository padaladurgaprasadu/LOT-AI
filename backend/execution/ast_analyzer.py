import ast
from typing import Dict, List, Any

class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1
        
    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)
        
    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)
        
    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)
        
    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)
        
    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)

def get_grade(score: int) -> str:
    if score <= 5: return 'A'
    if score <= 10: return 'B'
    if score <= 15: return 'C'
    if score <= 20: return 'D'
    return 'F'

def analyze_python(code: str) -> Dict[str, Any]:
    lines = code.split('\n')
    total_lines = len(lines)
    
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {'functions': [], 'issues': [f'SyntaxError: {e}'], 'overall_grade': 'F', 'total_lines': total_lines}
        
    functions = []
    issues = []
    
    if total_lines > 300:
        issues.append("File is too long (> 300 lines)")
        
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_lines = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
            if func_lines > 50:
                issues.append(f"Function {node.name} is too long (> 50 lines)")
                
            visitor = ComplexityVisitor()
            visitor.visit(node)
            comp = visitor.complexity
            
            # Simplified max nesting depth based on block size/comp
            if comp > 4:
                issues.append(f"Function {node.name} has nesting depth > 4 (based on complexity)")
            
            functions.append({
                'name': node.name,
                'lines': func_lines,
                'complexity': comp,
                'grade': get_grade(comp)
            })
            
    overall_comp = sum(f['complexity'] for f in functions) if functions else 0
    avg_comp = overall_comp / len(functions) if functions else 0
    overall_grade = get_grade(int(avg_comp))
    
    return {
        'functions': functions,
        'issues': issues,
        'overall_grade': overall_grade,
        'total_lines': total_lines
    }
