import subprocess
import time
import re
from typing import Dict, List

class PackageManager:
    def __init__(self):
        pass

    def install_python(self, packages: List[str], venv_path: str = None) -> Dict:
        pip_cmd = f"{venv_path}/bin/pip" if venv_path else "pip"
        cmd = [pip_cmd, "install"] + packages
        start = time.time()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "duration_ms": int((time.time() - start) * 1000)
            }
        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e), "duration_ms": int((time.time() - start) * 1000)}

    def install_node(self, packages: List[str], cwd: str = '.', dev: bool = False) -> Dict:
        cmd = ["npm", "install"]
        if dev:
            cmd.append("--save-dev")
        cmd.extend(packages)
        start = time.time()
        try:
            result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "duration_ms": int((time.time() - start) * 1000)
            }
        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e), "duration_ms": int((time.time() - start) * 1000)}

    def install_rust(self, crates: List[str]) -> Dict:
        cmd = ["cargo", "add"] + crates
        start = time.time()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "duration_ms": int((time.time() - start) * 1000)
            }
        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e), "duration_ms": int((time.time() - start) * 1000)}

    def check_installed(self, package: str, manager: str = 'pip') -> bool:
        if manager == 'pip':
            cmd = ["pip", "show", package]
        elif manager == 'npm':
            cmd = ["npm", "list", package]
        else:
            return False
            
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.returncode == 0
        except:
            return False

    def get_installed(self, manager: str = 'pip') -> List[Dict]:
        installed = []
        if manager == 'pip':
            try:
                result = subprocess.run(["pip", "list", "--format=json"], capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    import json
                    data = json.loads(result.stdout)
                    installed = [{"name": item["name"], "version": item["version"]} for item in data]
            except:
                pass
        return installed

    def detect_requirements(self, code: str) -> List[str]:
        reqs = set()
        patterns = [
            r"^\s*import\s+([a-zA-Z0-9_]+)",
            r"^\s*from\s+([a-zA-Z0-9_]+)\s+import"
        ]
        for line in code.split('\n'):
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    reqs.add(match.group(1))
        
        standard_libs = {"os", "sys", "re", "math", "time", "json", "typing", "subprocess", "collections", "datetime", "uuid"}
        return list(reqs - standard_libs)

def inject_package_manager_prompt(system_prompt: str) -> str:
    directive = "\n[PACKAGE MANAGER DIRECTIVE]: Manage dependencies autonomously across multiple environments."
    return system_prompt + directive
