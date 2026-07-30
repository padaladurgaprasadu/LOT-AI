from dataclasses import dataclass
from typing import List, Dict, Optional
import uuid

@dataclass
class Task:
    id: str
    title: str
    description: str
    priority: int
    status: str
    assigned_to: Optional[str]
    estimated_hours: int

@dataclass
class Sprint:
    number: int
    tasks: List[Task]
    start_date: str
    end_date: str

@dataclass
class Project:
    name: str
    description: str
    tech_stack: List[str]
    deadline: str

class ProjectManagerAgent:
    def __init__(self):
        pass

    def create_project(self, description: str) -> Project:
        return Project(
            name="Generated Project",
            description=description,
            tech_stack=["python", "react"],
            deadline="2027-01-01"
        )

    def generate_prd(self, project: Project) -> str:
        return f"""# Product Requirements Document
## Project: {project.name}
**Description:** {project.description}
**Tech Stack:** {', '.join(project.tech_stack)}
**Timeline:** {project.deadline}

## Goals
1. Deliver MVP
2. Scalable architecture

## User Stories
- As a user, I want to login.
"""

    def create_sprint(self, project: Project, sprint_num: int = 1, capacity_hours: int = 40) -> Sprint:
        tasks = [
            Task(id=str(uuid.uuid4()), title="Setup DB", description="Initialize DB", priority=1, status="TODO", assigned_to=None, estimated_hours=5),
            Task(id=str(uuid.uuid4()), title="Create API", description="Build REST API", priority=2, status="TODO", assigned_to=None, estimated_hours=15)
        ]
        return Sprint(number=sprint_num, tasks=tasks, start_date="today", end_date="next week")

    def assign_to_agents(self, sprint: Sprint) -> Dict[str, List[Task]]:
        assignments = {"backend": [], "frontend": []}
        for task in sprint.tasks:
            if "DB" in task.title or "API" in task.title:
                assignments["backend"].append(task)
            else:
                assignments["frontend"].append(task)
        return assignments

    def daily_standup(self, sprint: Sprint) -> str:
        return f"Sprint {sprint.number} Progress: All tasks on track."

    def estimate_task(self, task_description: str) -> Dict:
        return {"hours": 5, "complexity": 3, "risk": "low"}

    def generate_readme(self, project: Project) -> str:
        return f"# {project.name}\n\n{project.description}\n\nTech: {', '.join(project.tech_stack)}"

def inject_pm_prompt(system_prompt: str, task: str) -> str:
    return system_prompt + f"\n[PM DIRECTIVE]: Manage project task: {task}"
