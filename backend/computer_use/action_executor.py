import os
import json
import time
from typing import Dict, Any, Tuple
try:
    import pyautogui
except ImportError:
    pyautogui = None

class ActionExecutor:
    """Execute mouse and keyboard actions for computer automation."""
    def __init__(self):
        if pyautogui:
            pyautogui.FAILSAFE = True
        self.audit_log_path = os.path.join(os.path.dirname(__file__), 'action_audit.jsonl')

    def _log_action(self, action: str, details: Dict[str, Any]):
        os.makedirs(os.path.dirname(self.audit_log_path), exist_ok=True)
        with open(self.audit_log_path, 'a', encoding='utf-8') as f:
            log_entry = {"timestamp": time.time(), "action": action, "details": details}
            f.write(json.dumps(log_entry) + '\n')

    def is_safe_coordinate(self, x: int, y: int) -> bool:
        if not pyautogui: return False
        w, h = pyautogui.size()
        return 0 <= x < w and 0 <= y < h

    def click(self, x: int, y: int, button: str = 'left', clicks: int = 1) -> bool:
        if not pyautogui or not self.is_safe_coordinate(x, y):
            return False
        pyautogui.click(x=x, y=y, button=button, clicks=clicks)
        time.sleep(0.1)
        self._log_action("click", {"x": x, "y": y, "button": button, "clicks": clicks})
        return True

    def type_text(self, text: str, interval_s: float = 0.05) -> bool:
        if not pyautogui: return False
        pyautogui.write(text, interval=interval_s)
        time.sleep(0.1)
        self._log_action("type", {"text": text, "interval": interval_s})
        return True

    def press_key(self, key: str) -> bool:
        if not pyautogui: return False
        pyautogui.press(key)
        time.sleep(0.1)
        self._log_action("press_key", {"key": key})
        return True

    def hotkey(self, *keys) -> bool:
        if not pyautogui: return False
        pyautogui.hotkey(*keys)
        time.sleep(0.1)
        self._log_action("hotkey", {"keys": keys})
        return True

    def scroll(self, x: int, y: int, clicks: int = 3, direction: str = 'down') -> bool:
        if not pyautogui or not self.is_safe_coordinate(x, y):
            return False
        pyautogui.moveTo(x, y)
        amount = -clicks * 100 if direction == 'down' else clicks * 100
        pyautogui.scroll(amount)
        time.sleep(0.1)
        self._log_action("scroll", {"x": x, "y": y, "clicks": clicks, "direction": direction})
        return True

    def drag(self, from_x: int, from_y: int, to_x: int, to_y: int, duration_s: float = 0.5) -> bool:
        if not pyautogui or not self.is_safe_coordinate(from_x, from_y) or not self.is_safe_coordinate(to_x, to_y):
            return False
        pyautogui.moveTo(from_x, from_y)
        pyautogui.dragTo(to_x, to_y, duration=duration_s, button='left')
        time.sleep(0.1)
        self._log_action("drag", {"from": (from_x, from_y), "to": (to_x, to_y), "duration": duration_s})
        return True

    def get_mouse_position(self) -> Tuple[int, int]:
        if not pyautogui: return (0, 0)
        return pyautogui.position()

def inject_action_executor_prompt(system_prompt: str) -> str:
    return system_prompt + "\n\n[Action Executor Ready: Can control mouse and keyboard safely.]"
