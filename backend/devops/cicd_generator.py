class CICDGenerator:
    def __init__(self):
        pass

    def generate_github_actions(self, tech_stack: str, deploy_target: str = 'railway') -> str:
        return f"""name: CI/CD Pipeline
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup {tech_stack}
        uses: actions/setup-{tech_stack.lower()}@v3
      - name: Install Dependencies
        run: |
          npm ci || pip install -r requirements.txt
      - name: Run Tests
        run: npm test || pytest
      - name: Security Scan
        run: npx eslint-security || pip install bandit && bandit -r .
      - name: Deploy to {deploy_target}
        run: echo "Deploying to {deploy_target}"
"""

    def generate_gitlab_ci(self, tech_stack: str) -> str:
        return f"""stages:
  - test
  - build
  - deploy

test_job:
  stage: test
  script:
    - echo "Testing {tech_stack}"
"""

    def generate_dockerfile_for_stack(self, stack: str) -> str:
        if stack.lower() == 'python':
            return "FROM python:3.12\nCOPY . .\nCMD ['python', 'main.py']"
        return "FROM ubuntu:latest\nCMD ['echo', 'Hello']"

    def get_railway_deploy_script(self) -> str:
        return "railway up --detach"

    def get_vercel_deploy_script(self) -> str:
        return "vercel --prod"

    def generate_k8s_manifests(self, app_name: str, image: str, port: int, replicas: int = 2) -> str:
        return f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: {image}
        ports:
        - containerPort: {port}
---
apiVersion: v1
kind: Service
metadata:
  name: {app_name}-svc
spec:
  selector:
    app: {app_name}
  ports:
    - port: 80
      targetPort: {port}
"""

def inject_cicd_prompt(system_prompt: str) -> str:
    return system_prompt + "\n[CICD DIRECTIVE]: Generate robust CI/CD pipelines automatically."
