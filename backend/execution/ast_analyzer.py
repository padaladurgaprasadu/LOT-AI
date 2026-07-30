"""
Real Python AST analysis engine.
Analyzes Python code for cyclomatic complexity, length, dead code patterns, and issues.
"""

import ast

def _compute_complexity(node: ast.AST) -> int:
    complexity = 1
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler, ast.BoolOp)):
            if isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            else:
                complexity += 1
    return complexity

def _compute_nesting_depth(node: ast.AST) -> int:
    max_depth = 0
    for child in ast.iter_child_nodes(node):
        max_depth = max(max_depth, _compute_nesting_depth(child) + 1)
    return max_depth

def analyze_python(code: str) -> dict:
    """Analyzes Python code string for complexity and issues."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {
            "complexity_score": 0,
            "issues": [f"SyntaxError: {str(e)}"],
            "functions": [],
            "overall_grade": "F"
        }

    issues = []
    functions = []
    total_complexity = _compute_complexity(tree)

    imports = set()
    used_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.add(alias.asname or alias.name)
        elif isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):
                used_names.add(node.id)

    unused_imports = imports - used_names
    for ui in unused_imports:
        issues.append(f"Unused import: {ui}")

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start_line = node.lineno
            end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
            lines = end_line - start_line + 1
            
            func_complexity = _compute_complexity(node)
            func_depth = _compute_nesting_depth(node)

            functions.append({
                "name": node.name,
                "lines": lines,
                "complexity": func_complexity
            })

            if lines > 50:
                issues.append(f"Function {node.name} is too long ({lines} lines).")
            if func_depth > 4:
                issues.append(f"Function {node.name} has deep nesting (depth {func_depth}).")
            if func_complexity > 10:
                issues.append(f"Function {node.name} is too complex (score {func_complexity}).")

    score_val = max(0, 100 - total_complexity - len(issues) * 5)
    grade = "A" if score_val > 90 else "B" if score_val > 80 else "C" if score_val > 70 else "D" if score_val > 60 else "F"

    return {
        "complexity_score": total_complexity,
        "issues": issues,
        "functions": functions,
        "overall_grade": grade
    }

def analyze_file(filepath: str) -> dict:
    """Analyzes a Python file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        return analyze_python(code)
    except Exception as e:
        return {
            "complexity_score": 0,
            "issues": [f"File read error: {str(e)}"],
            "functions": [],
            "overall_grade": "F"
        }

def inject_ast_analysis_prompt(system_prompt: str) -> str:
    """Injects AST analysis directive into system prompt."""
    directive = "\n[AST DIRECTIVE]: Write clean code. Max complexity 10, max nesting 4, max lines 50 per function.\n"
    return system_prompt + directive
