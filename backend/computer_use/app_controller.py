import os
import subprocess
import platform
import time
import base64
from typing import Dict, Any, List
try:
    import psutil
except ImportError:
    psutil = None
try:
    import pyperclip
except ImportError:
    pyperclip = None

class AppController:
    """High-level application control — open apps, control VS Code, Terminal, browsers."""
    def __init__(self):
        self.os_type = platform.system()

    def open_application(self, app_name: str) -> Dict[str, Any]:
        try:
            if self.os_type == "Windows":
                proc = subprocess.Popen(["start", app_name], shell=True)
            elif self.os_type == "Darwin":
                proc = subprocess.Popen(["open", "-a", app_name])
            else:
                proc = subprocess.Popen([app_name])
            return {"success": True, "pid": proc.pid, "window_title": app_name}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_terminal(self, cwd: str = None) -> Dict[str, Any]:
        try:
            if self.os_type == "Windows":
                proc = subprocess.Popen(["start", "cmd.exe"], cwd=cwd, shell=True)
            elif self.os_type == "Darwin":
                proc = subprocess.Popen(["open", "-a", "Terminal", cwd or "."])
            else:
                proc = subprocess.Popen(["x-terminal-emulator"], cwd=cwd)
            return {"success": True, "pid": proc.pid}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def open_vscode(self, folder: str = None, file: str = None) -> bool:
        target = file or folder or "."
        try:
            subprocess.Popen(["code", target], shell=(self.os_type == "Windows"))
            return True
        except Exception:
            return False

    def open_browser(self, url: str, browser: str = 'default') -> bool:
        import webbrowser
        try:
            if browser == 'default':
                webbrowser.open(url)
            else:
                webbrowser.get(browser).open(url)
            return True
        except Exception:
            return False

    def close_application(self, app_name_or_pid: str) -> bool:
        if not psutil: return False
        try:
            if str(app_name_or_pid).isdigit():
                psutil.Process(int(app_name_or_pid)).terminate()
                return True
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and app_name_or_pid.lower() in proc.info['name'].lower():
                    proc.terminate()
                    return True
        except Exception:
            pass
        return False

    def list_running_apps(self) -> List[Dict[str, Any]]:
        if not psutil: return []
        apps = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                mem = proc.info['memory_info'].rss / (1024 * 1024) if proc.info['memory_info'] else 0
                apps.append({"name": proc.info['name'], "pid": proc.info['pid'], "memory_mb": round(mem, 2)})
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return sorted(apps, key=lambda x: x["memory_mb"], reverse=True)[:50]

    def focus_window(self, window_title: str) -> bool:
        # Cross-platform window focus requires native bindings.
        # Fallback to simple stub.
        return True

    def get_clipboard(self) -> str:
        if pyperclip:
            return pyperclip.paste()
        return ""

    def set_clipboard(self, text: str) -> bool:
        if pyperclip:
            pyperclip.copy(text)
            return True
        return False

    def take_app_screenshot(self, app_name: str) -> str:
        # Stub for app-specific screenshot
        return "base64_screenshot_placeholder"

def inject_app_controller_prompt(system_prompt: str) -> str:
    return system_prompt + "\n\n[App Controller Ready: Manage VS Code, browsers, terminals.]"
