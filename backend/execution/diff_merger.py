"""
Git-style clean diff generator using Python's difflib.
"""

import difflib

def compute_diff(original: str, patched: str, filename: str = 'file') -> dict:
    """Computes a unified diff between two strings."""
    original_lines = original.splitlines(keepends=True)
    patched_lines = patched.splitlines(keepends=True)
    
    diff_gen = difflib.unified_diff(
        original_lines, 
        patched_lines, 
        fromfile=f"a/{filename}", 
        tofile=f"b/{filename}",
        n=3
    )
    
    unified_diff = "".join(diff_gen)
    
    added_count = 0
    removed_count = 0
    
    for line in unified_diff.splitlines():
        if line.startswith('+') and not line.startswith('+++'):
            added_count += 1
        elif line.startswith('-') and not line.startswith('---'):
            removed_count += 1
            
    change_summary = f"+{added_count} additions, -{removed_count} deletions"
    
    return {
        "original_lines": len(original_lines),
        "patched_lines": len(patched_lines),
        "unified_diff": unified_diff,
        "added_count": added_count,
        "removed_count": removed_count,
        "change_summary": change_summary
    }

def format_diff_for_display(diff_dict: dict) -> str:
    """Pretty-prints the diff."""
    if not diff_dict['unified_diff']:
        return "No changes."
    
    header = f"Changes: {diff_dict['change_summary']}\n"
    header += "=" * 40 + "\n"
    return header + diff_dict['unified_diff']

def inject_diff_merger_prompt(system_prompt: str) -> str:
    """Injects diff merger directive into the system prompt."""
    directive = "\n[DIFF DIRECTIVE]: Ensure changes are minimal and preserve surrounding formatting.\n"
    return system_prompt + directive
