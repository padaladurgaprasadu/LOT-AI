"""
AST-level automatic error repair engine.
Parses Python tracebacks and applies repairs to code.
"""

import re
import ast

def heal_python_error(code: str, error_output: str) -> dict:
    """Parses traceback and attempts to heal the code."""
    patched_code = code
    repair_applied = "None"
    confidence = 0.0
    success = False

    error_match = re.search(r"(NameError|TypeError|AttributeError|IndentationError|ImportError|SyntaxError):\s*(.*)", error_output)
    line_match = re.search(r"line (\d+)", error_output)
    
    if error_match and line_match:
        error_type = error_match.group(1)
        error_msg = error_match.group(2)
        line_num = int(line_match.group(1)) - 1
        
        lines = code.split('\n')
        if line_num < len(lines):
            target_line = lines[line_num]

            if error_type == "NameError":
                match = re.search(r"name '(\w+)' is not defined", error_msg)
                if match:
                    var_name = match.group(1)
                    if var_name in ["os", "sys", "json", "re", "math", "datetime"]:
                        patched_code = f"import {var_name}\n" + code
                        repair_applied = f"Injected import {var_name}"
                        confidence = 0.9
                        success = True
                    else:
                        lines.insert(line_num, f"{' ' * (len(target_line) - len(target_line.lstrip()))}{var_name} = None")
                        patched_code = '\n'.join(lines)
                        repair_applied = f"Injected default variable definition for {var_name}"
                        confidence = 0.6
                        success = True

            elif error_type == "TypeError":
                if "int() argument must be a string" in error_msg or "can only concatenate str" in error_msg:
                    patched_code = code.replace(target_line, target_line.replace("+", " + str("))
                    repair_applied = "Attempted type conversion wrapping"
                    confidence = 0.4
                    success = True

            elif error_type == "AttributeError":
                if "'NoneType' object has no attribute" in error_msg:
                    match = re.search(r"attribute '(\w+)'", error_msg)
                    if match:
                        attr = match.group(1)
                        indent = ' ' * (len(target_line) - len(target_line.lstrip()))
                        patched_code = '\n'.join(lines[:line_num] + [f"{indent}if locals().get('obj') is not None:", target_line] + lines[line_num+1:])
                        repair_applied = "Injected None guard check"
                        confidence = 0.3
                        success = False

            elif error_type == "IndentationError":
                patched_code = code.replace("\t", "    ")
                repair_applied = "Re-indented block (replaced tabs with spaces)"
                confidence = 0.8
                success = True

            elif error_type == "ImportError":
                match = re.search(r"No module named '(\w+)'", error_msg)
                if match:
                    repair_applied = f"Suggest running: pip install {match.group(1)}"
                    confidence = 0.95
                    success = False

            elif error_type == "SyntaxError":
                try:
                    ast.parse(code)
                except SyntaxError:
                    repair_applied = "Attempted AST-based reformat (failed)"
                    confidence = 0.1
                    success = False

    return {
        "patched_code": patched_code,
        "repair_applied": repair_applied,
        "confidence": confidence,
        "success": success
    }

def inject_self_healing_prompt(system_prompt: str) -> str:
    """Injects self-healing directive into the system prompt."""
    directive = "\n[HEALING DIRECTIVE]: Write fault-tolerant code. Check types and handle None appropriately.\n"
    return system_prompt + directive
