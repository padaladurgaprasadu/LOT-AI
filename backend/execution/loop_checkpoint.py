"""
Crash-safe loop state persistence.
Saves and loads state checkpoints in JSON format.
"""

import json
import os
import time
from typing import Optional

CHECKPOINT_DIR = os.path.join(os.path.dirname(__file__), "checkpoints")

def _ensure_dir():
    if not os.path.exists(CHECKPOINT_DIR):
        os.makedirs(CHECKPOINT_DIR)

def save_checkpoint(task_id: str, state: dict) -> None:
    """Saves loop state as JSON."""
    _ensure_dir()
    filepath = os.path.join(CHECKPOINT_DIR, f"{task_id}.json")
    
    state['last_checkpoint_at'] = time.time()
    
    # Write to a temporary file first for crash safety
    temp_filepath = f"{filepath}.tmp"
    with open(temp_filepath, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=4)
        
    os.replace(temp_filepath, filepath)

def load_checkpoint(task_id: str) -> Optional[dict]:
    """Loads loop state from JSON."""
    filepath = os.path.join(CHECKPOINT_DIR, f"{task_id}.json")
    if not os.path.exists(filepath):
        return None
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None

def clear_checkpoint(task_id: str) -> None:
    """Clears the checkpoint for a task."""
    filepath = os.path.join(CHECKPOINT_DIR, f"{task_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)

def inject_checkpoint_prompt(system_prompt: str) -> str:
    """Injects checkpoint directive into the system prompt."""
    directive = "\n[CHECKPOINT DIRECTIVE]: The execution loop is persistent. State is saved automatically.\n"
    return system_prompt + directive
