"""
Automation task recorder and replayer for PrismAI.
"""
from dataclasses import dataclass
from typing import Dict, Any, List
import time
import json
import os
import uuid

@dataclass
class AutomationStep:
    type: str
    params: Dict[str, Any]
    timestamp: float
    screenshot_b64: str = None
    
    def to_dict(self):
        return {
            "type": self.type,
            "params": self.params,
            "timestamp": self.timestamp,
            "screenshot_b64": self.screenshot_b64
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            type=data["type"],
            params=data["params"],
            timestamp=data["timestamp"],
            screenshot_b64=data.get("screenshot_b64")
        )

class TaskRecorder:
    """Records and replays computer interaction tasks."""
    
    def __init__(self):
        self.sessions: Dict[str, List[AutomationStep]] = {}
        self.automations_dir = os.path.join(os.path.dirname(__file__), "automations")
        os.makedirs(self.automations_dir, exist_ok=True)

    def start_recording(self, task_name: str) -> str:
        """Begins recording a task and returns a session ID."""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = []
        return session_id

    def record_step(self, session_id: str, step: AutomationStep) -> bool:
        """Records a single automation step."""
        if session_id in self.sessions:
            self.sessions[session_id].append(step)
            return True
        return False

    def stop_recording(self, session_id: str) -> List[AutomationStep]:
        """Stops recording and returns the recorded steps."""
        return self.sessions.pop(session_id, [])

    def save_automation(self, session_id: str, name: str) -> str:
        """Saves a session to disk."""
        if session_id not in self.sessions:
            return "Session not found."
            
        steps = self.sessions[session_id]
        path = os.path.join(self.automations_dir, f"{name}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump([s.to_dict() for s in steps], f, indent=2)
            
        return path

    def load_automation(self, name: str) -> List[AutomationStep]:
        """Loads a saved automation from disk."""
        path = os.path.join(self.automations_dir, f"{name}.json")
        if not os.path.exists(path):
            return []
            
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [AutomationStep.from_dict(d) for d in data]

    def replay_automation(self, name: str, speed: float = 1.0) -> Dict[str, Any]:
        """Replays a saved automation."""
        steps = self.load_automation(name)
        if not steps:
            return {"steps_executed": 0, "errors": ["Automation not found"], "duration_s": 0}
            
        start_time = time.time()
        executed = 0
        
        # Mock replay
        for step in steps:
            time.sleep(0.1 / speed)
            executed += 1
            
        return {
            "steps_executed": executed,
            "errors": [],
            "duration_s": time.time() - start_time
        }

    def generate_script(self, steps: List[AutomationStep], language: str = 'python') -> str:
        """Generates a Python script using pyautogui from steps."""
        script = ["import pyautogui", "import time", ""]
        
        for i, step in enumerate(steps):
            if step.type == "click":
                x = step.params.get("x", 0)
                y = step.params.get("y", 0)
                script.append(f"pyautogui.click(x={x}, y={y})")
            elif step.type == "type":
                text = step.params.get("text", "")
                script.append(f"pyautogui.write('{text}')")
            elif step.type == "keyboard_shortcut":
                keys = step.params.get("keys", [])
                keys_str = ", ".join([f"'{k}'" for k in keys])
                script.append(f"pyautogui.hotkey({keys_str})")
            elif step.type == "wait":
                seconds = step.params.get("seconds", 1)
                script.append(f"time.sleep({seconds})")
                
        return "\n".join(script)

    def list_automations(self) -> List[str]:
        """Lists all saved automations."""
        if not os.path.exists(self.automations_dir):
            return []
        return [f.replace(".json", "") for f in os.listdir(self.automations_dir) if f.endswith(".json")]


def inject_recorder_prompt(system_prompt: str) -> str:
    """Adds recorder context to system prompt."""
    return f"{system_prompt}\n[Recorder Context]: PrismAI can record and replay sequences of GUI actions."
