"""
LOT AI JCode Core Integration Engine
======================================
Inspired by 1jehuang/jcode (https://github.com/1jehuang/jcode).
Integrates AST-aware code navigation, dependency graph indexing, 
and surgical Tree-Sitter code modification capabilities.
"""

def inject_jcode_prompt(system_prompt: str) -> str:
    """
    Injects JCode AST code indexing & surgical editing directives.
    """
    jcode_prompt = "\n\n[💻 LOTAI JCODE AST & DEPENDENCY ENGINE (1jehuang/jcode Architecture)]:\n"
    jcode_prompt += "• AST-Aware Surgical Editing: Uses Abstract Syntax Tree (AST) parsing to locate & edit specific functions/classes without full-file rewrites.\n"
    jcode_prompt += "• Codebase Dependency Graph: Indexes all imports, exports, and call graphs across multi-file repositories.\n"
    jcode_prompt += "• Fast Terminal CLI Harness: Intercepts and executes CLI commands, test runners, and git operations with zero-latency streaming.\n\n"
    
    return system_prompt + jcode_prompt
