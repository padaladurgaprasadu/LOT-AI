import subprocess
import time
import uuid
import tempfile
import os
from typing import Dict, List

class DockerVMEngine:
    def __init__(self):
        pass

    def create_session(self, task_id: str, stack: str = 'python') -> Dict:
        cmd = [
            "docker", "run", "-d", f"--name=prismai_{task_id}",
            "--memory=512m", "--cpus=0.5", "--network=none",
            "python:3.12-slim", "sleep", "infinity"
        ]
        try:
            start = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "duration_ms": int((time.time() - start) * 1000)
            }
        except subprocess.TimeoutExpired as e:
            return {"stdout": "", "stderr": str(e), "exit_code": -1, "duration_ms": 60000}
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "exit_code": -1, "duration_ms": 0}

    def exec_in_container(self, task_id: str, cmd: str) -> Dict:
        docker_cmd = ["docker", "exec", f"prismai_{task_id}", "sh", "-c", cmd]
        try:
            start = time.time()
            result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=60)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "duration_ms": int((time.time() - start) * 1000)
            }
        except subprocess.TimeoutExpired as e:
            return {"stdout": "", "stderr": str(e), "exit_code": -1, "duration_ms": 60000}
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "exit_code": -1, "duration_ms": 0}

    def install_packages(self, task_id: str, packages: List[str], manager: str = 'pip') -> Dict:
        cmd = f"{manager} install " + " ".join(packages)
        return self.exec_in_container(task_id, cmd)

    def copy_code(self, task_id: str, code: str, filename: str = 'main.py') -> bool:
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
                f.write(code)
                temp_path = f.name
            
            cmd = ["docker", "cp", temp_path, f"prismai_{task_id}:/{filename}"]
            subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            os.remove(temp_path)
            return True
        except Exception:
            return False

    def run_code(self, task_id: str, filename: str = 'main.py') -> Dict:
        cmd = f"python /{filename}"
        return self.exec_in_container(task_id, cmd)

    def destroy_session(self, task_id: str) -> bool:
        cmd = ["docker", "rm", "-f", f"prismai_{task_id}"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return result.returncode == 0
        except Exception:
            return False

    def list_sessions(self) -> List[str]:
        cmd = ["docker", "ps", "--filter", "name=prismai", "--format", "{{.Names}}"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                names = result.stdout.strip().split('\n')
                return [name.replace("prismai_", "") for name in names if name]
            return []
        except Exception:
            return []

def inject_docker_vm_prompt(system_prompt: str) -> str:
    docker_directive = "\n[DOCKER VM DIRECTIVE]: You have access to isolated Docker VMs. Spin them up for execution and testing."
    return system_prompt + docker_directive
