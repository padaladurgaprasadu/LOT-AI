from dataclasses import dataclass
from typing import List, Dict

@dataclass
class AgentJob:
    agent_type: str
    task_description: str
    dependencies: List[str]
    status: str
    result: str

class MultiAgentCoordinator:
    def __init__(self):
        pass

    def decompose_to_jobs(self, project_description: str) -> List[AgentJob]:
        return [
            AgentJob(agent_type="backend", task_description="Build API", dependencies=[], status="pending", result=""),
            AgentJob(agent_type="frontend", task_description="Build UI", dependencies=["Build API"], status="pending", result="")
        ]

    def get_execution_order(self, jobs: List[AgentJob]) -> List[List[AgentJob]]:
        # Dummy topological sort
        layer1 = [j for j in jobs if not j.dependencies]
        layer2 = [j for j in jobs if j.dependencies]
        return [layer1, layer2]

    def simulate_execution(self, jobs: List[AgentJob]) -> Dict:
        return {"status": "success", "time_taken": 100}

    def build_coordination_prompt(self, jobs: List[AgentJob]) -> str:
        return "Coordinate the following jobs: " + ", ".join([j.task_description for j in jobs])

    def get_agent_specialties(self) -> Dict[str, List[str]]:
        return {
            "frontend": ["react", "vue", "angular", "css", "ui", "ux", "tailwind", "nextjs"],
            "backend": ["api", "database", "auth", "caching", "queues", "microservices"],
            "devops": ["docker", "kubernetes", "cicd", "monitoring", "cloud", "terraform"],
            "qa": ["testing", "e2e", "unit", "integration", "performance", "security"],
            "data": ["analytics", "ml", "etl", "visualization", "postgresql", "mongodb"]
        }

def inject_multi_agent_prompt(system_prompt: str) -> str:
    return system_prompt + "\n[MULTI-AGENT DIRECTIVE]: Coordinate effectively."
