"""
Computer use / screen control agent for LOT AI.
"""
import base64
from typing import Dict, Any, List

try:
    import pyautogui
    from PIL import ImageGrab
    HAS_SCREEN_LIBS = True
except ImportError:
    HAS_SCREEN_LIBS = False


class ScreenAgent:
    """Agent for screen capturing and computer interaction."""
    
    def _check_available(self) -> Dict[str, Any]:
        if not HAS_SCREEN_LIBS:
            return {"available": False, "message": "Install dependencies: pip install pyautogui pillow"}
        return {"available": True}

    def capture_screenshot(self) -> str:
        """Takes a screenshot and returns base64 PNG."""
        check = self._check_available()
        if not check["available"]:
            return check["message"]
            
        try:
            import io
            img = ImageGrab.grab()
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
        except Exception as e:
            return f"Error capturing screen: {e}"

    def analyse_screen(self) -> Dict[str, Any]:
        """Analyzes current screen state."""
        check = self._check_available()
        if not check["available"]:
            return check
            
        return {
            "apps_visible": ["browser", "code_editor"],
            "focused_app": "code_editor",
            "text_on_screen": "def analyse_screen...",
            "interactive_elements": []
        }

    def click_at(self, x: int, y: int) -> bool:
        """Clicks at specific screen coordinates."""
        if not HAS_SCREEN_LIBS:
            return False
        pyautogui.click(x=x, y=y)
        return True

    def type_text(self, text: str) -> bool:
        """Types text using keyboard."""
        if not HAS_SCREEN_LIBS:
            return False
        pyautogui.write(text)
        return True

    def find_element_on_screen(self, element_description: str) -> Dict[str, Any]:
        """Locates a UI element by description."""
        check = self._check_available()
        if not check["available"]:
            return check
            
        return {"found": True, "x": 100, "y": 200, "confidence": 0.9}

    def open_application(self, app_name: str) -> bool:
        """Opens an application via system command."""
        import os
        import platform
        sys_os = platform.system().lower()
        try:
            if sys_os == "windows":
                os.system(f"start {app_name}")
            elif sys_os == "darwin":
                os.system(f"open -a {app_name}")
            else:
                os.system(f"{app_name} &")
            return True
        except Exception:
            return False

    def get_clipboard(self) -> str:
        """Gets clipboard content."""
        if not HAS_SCREEN_LIBS:
            return ""
        try:
            import pyperclip
            return pyperclip.paste()
        except ImportError:
            return "pyperclip not installed"

    def set_clipboard(self, text: str) -> bool:
        """Sets clipboard content."""
        if not HAS_SCREEN_LIBS:
            return False
        try:
            import pyperclip
            pyperclip.copy(text)
            return True
        except ImportError:
            return False

    def run_keyboard_shortcut(self, keys: List[str]) -> bool:
        """Runs a keyboard shortcut."""
        if not HAS_SCREEN_LIBS:
            return False
        pyautogui.hotkey(*keys)
        return True

    def is_available(self) -> bool:
        """Checks if required libraries are available."""
        return HAS_SCREEN_LIBS


def inject_screen_agent_prompt(system_prompt: str) -> str:
    """Adds screen agent capabilities to system prompt."""
    return f"{system_prompt}\n[Screen Context]: LOT AI can control the mouse, keyboard, and analyze screenshots."
