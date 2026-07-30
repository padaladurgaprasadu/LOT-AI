import subprocess
import time
import sys
import platform
import re
from typing import Dict, Generator

class TerminalEngine:
    def __init__(self):
        pass

    def run(self, cmd: str, cwd: str = None, timeout: int = 30, shell: bool = True) -> Dict:
        if not self.is_safe_command(cmd):
            return {"stdout": "", "stderr": "Command blocked for safety reasons.", "exit_code": 1, "duration_ms": 0}
        
        try:
            start = time.time()
            result = subprocess.run(cmd, cwd=cwd, shell=shell, capture_output=True, text=True, timeout=timeout)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "duration_ms": int((time.time() - start) * 1000)
            }
        except subprocess.TimeoutExpired as e:
            return {"stdout": "", "stderr": str(e), "exit_code": -1, "duration_ms": int(timeout * 1000)}
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "exit_code": -1, "duration_ms": 0}

    def run_stream(self, cmd: str) -> Generator[str, None, None]:
        if not self.is_safe_command(cmd):
            yield "Command blocked for safety reasons."
            return

        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                yield line.strip()
            process.wait()
        except Exception as e:
            yield str(e)

    def is_safe_command(self, cmd: str) -> bool:
        cmd_lower = cmd.lower()
        blocked_patterns = [
            r"rm\s+-rf\s+/", r"dd\s+if=/dev/zero", r"\bmkfs\b", r"\bformat\b",
            r"drop\s+table\b(?!\s+where)", r"delete\s+from\b(?!\s+where)"
        ]
        for pattern in blocked_patterns:
            if re.search(pattern, cmd_lower):
                return False
        return True

    def get_env_info(self) -> Dict:
        env_info = {
            "os": platform.system(),
            "python_version": sys.version,
            "node_version": "unknown",
            "git_version": "unknown",
            "docker_version": "unknown"
        }
        
        try:
            node_res = subprocess.run(["node", "-v"], capture_output=True, text=True, timeout=5)
            if node_res.returncode == 0:
                env_info["node_version"] = node_res.stdout.strip()
        except: pass
        
        try:
            git_res = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=5)
            if git_res.returncode == 0:
                env_info["git_version"] = git_res.stdout.strip()
        except: pass
        
        try:
            docker_res = subprocess.run(["docker", "--version"], capture_output=True, text=True, timeout=5)
            if docker_res.returncode == 0:
                env_info["docker_version"] = docker_res.stdout.strip()
        except: pass
        
        return env_info

def inject_terminal_prompt(system_prompt: str) -> str:
    terminal_directive = "\n[TERMINAL DIRECTIVE]: You have access to a secure terminal. Ensure commands are safe before execution."
    return system_prompt + terminal_directive
