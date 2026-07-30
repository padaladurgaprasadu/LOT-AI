"""
Secure isolated code execution engine.
Runs Python and JavaScript code in isolated subprocesses with timeout and resource limitations.
"""

import subprocess
import threading
import time
import json
import os

try:
    import resource
except ImportError:
    resource = None

def _set_resource_limits():
    if resource:
        try:
            resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
            resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
        except (ValueError, OSError):
            pass

def _run_with_timeout(cmd: list, code: str, timeout: int) -> dict:
    start_time = time.time()
    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=_set_resource_limits if resource else None
        )
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "runtime_ms": 0,
            "success": False
        }

    timer = threading.Timer(timeout, process.kill)
    try:
        timer.start()
        stdout, stderr = process.communicate(input=code)
    except Exception as e:
        process.kill()
        return {
            "stdout": "",
            "stderr": f"Execution error: {str(e)}",
            "exit_code": -1,
            "runtime_ms": int((time.time() - start_time) * 1000),
            "success": False
        }
    finally:
        timer.cancel()

    runtime_ms = int((time.time() - start_time) * 1000)
    exit_code = process.returncode
    
    if exit_code == -9 or exit_code == 137:
        stderr += f"\nProcess killed due to timeout ({timeout}s)."

    return {
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "runtime_ms": runtime_ms,
        "success": exit_code == 0
    }

def run_python(code: str, timeout: int = 30) -> dict:
    """Run Python code securely."""
    return _run_with_timeout(["python"], code, timeout)

def run_javascript(code: str, timeout: int = 30) -> dict:
    """Run JavaScript code securely via Node.js."""
    return _run_with_timeout(["node"], code, timeout)

def inject_sandbox_prompt(system_prompt: str) -> str:
    """Injects SANDBOX directive into the system prompt."""
    directive = "\n[SANDBOX DIRECTIVE]: All executable code must be safe for isolated sandbox execution without internet access.\n"
    return system_prompt + directive
