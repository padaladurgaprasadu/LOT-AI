import subprocess
import time
import json
import urllib.request
import tempfile
import os
from typing import Dict, List

class DockerBuildEngine:
    def __init__(self):
        pass

    def generate_dockerfile(self, tech_stack: str, entry_point: str, port: int = 8000) -> str:
        if tech_stack.lower() == 'python':
            return f"""FROM python:3.12-slim
RUN useradd -m appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE {port}
CMD ["gunicorn", "-b", "0.0.0.0:{port}", "{entry_point}"]
"""
        elif tech_stack.lower() == 'node':
            return f"""FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/package*.json ./
RUN npm ci --production
COPY --from=builder /app/dist ./dist
EXPOSE {port}
CMD ["node", "{entry_point}"]
"""
        elif tech_stack.lower() == 'react':
            return f"""FROM nginx:alpine
COPY build/ /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
        return "FROM ubuntu:latest\nCMD ['echo', 'Not implemented']"

    def build_image(self, dockerfile_content: str, tag: str, context_path: str = '.') -> Dict:
        start_time = time.time()
        try:
            with tempfile.NamedTemporaryFile(mode='w', dir=context_path, delete=False, suffix='Dockerfile') as f:
                f.write(dockerfile_content)
                df_path = f.name
            
            cmd = ["docker", "build", "-t", tag, "-f", df_path, context_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            os.remove(df_path)
            
            success = result.returncode == 0
            return {
                "success": success,
                "image_id": tag if success else "",
                "size_mb": 0.0, # Placeholder
                "duration_s": time.time() - start_time
            }
        except Exception as e:
            return {"success": False, "image_id": "", "size_mb": 0.0, "duration_s": time.time() - start_time}

    def push_to_registry(self, tag: str, registry: str = 'ghcr.io') -> Dict:
        cmd = ["docker", "push", f"{registry}/{tag}"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return {
                "success": result.returncode == 0,
                "pushed_tag": f"{registry}/{tag}",
                "digest": "sha256:dummy"
            }
        except Exception:
            return {"success": False, "pushed_tag": "", "digest": ""}

    def run_container(self, tag: str, port: int = 8000, env_vars: Dict = None) -> Dict:
        cmd = ["docker", "run", "-d", "-p", f"{port}:{port}"]
        if env_vars:
            for k, v in env_vars.items():
                cmd.extend(["-e", f"{k}={v}"])
        cmd.append(tag)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                return {"container_id": result.stdout.strip(), "url": f"http://localhost:{port}"}
            return {"container_id": "", "url": ""}
        except Exception:
            return {"container_id": "", "url": ""}

    def health_check(self, url: str, retries: int = 5) -> bool:
        for i in range(retries):
            try:
                req = urllib.request.Request(f"{url}/health")
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.getcode() == 200:
                        return True
            except Exception:
                time.sleep(2 ** i)
        return False

    def generate_compose(self, services: List[Dict]) -> str:
        compose = "version: '3.8'\nservices:\n"
        for srv in services:
            compose += f"  {srv.get('name', 'app')}:\n"
            compose += f"    image: {srv.get('image', 'ubuntu')}\n"
            if 'ports' in srv:
                compose += f"    ports:\n"
                for p in srv['ports']:
                    compose += f"      - '{p}'\n"
        return compose

def inject_docker_engine_prompt(system_prompt: str) -> str:
    return system_prompt + "\n[DOCKER BUILD DIRECTIVE]: Automate containerization."
