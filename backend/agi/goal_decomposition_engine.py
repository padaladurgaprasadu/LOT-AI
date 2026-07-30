"""
Hierarchical goal DAG planner.
Decomposes high-level goals into parallelizable sub-goals.
"""
from typing import List, Dict, Any

class Goal:
    def __init__(self, goal_id: str, description: str, dependencies: List[str], success_criteria: str, estimated_complexity: int):
        self.id = goal_id
        self.description = description
        self.dependencies = dependencies
        self.success_criteria = success_criteria
        self.estimated_complexity = estimated_complexity
        self.status = "PENDING"

class GoalDAG:
    def __init__(self):
        self.goals: Dict[str, Goal] = {}
        
    def add_goal(self, goal: Goal):
        self.goals[goal.id] = goal
        
    def add_dependency(self, goal_id: str, depends_on_id: str):
        if goal_id in self.goals and depends_on_id in self.goals:
            if depends_on_id not in self.goals[goal_id].dependencies:
                self.goals[goal_id].dependencies.append(depends_on_id)
                
    def topological_sort(self) -> List[str]:
        in_degree = {g_id: len(g.dependencies) for g_id, g in self.goals.items()}
        queue = [g_id for g_id, deg in in_degree.items() if deg == 0]
        sorted_goals = []
        
        while queue:
            curr = queue.pop(0)
            sorted_goals.append(curr)
            
            for g_id, g in self.goals.items():
                if curr in g.dependencies:
                    in_degree[g_id] -= 1
                    if in_degree[g_id] == 0:
                        queue.append(g_id)
                        
        return sorted_goals

    def get_parallel_groups(self) -> List[List[str]]:
        groups = []
        in_degree = {g_id: len(g.dependencies) for g_id, g in self.goals.items()}
        
        while True:
            current_group = [g_id for g_id, deg in in_degree.items() if deg == 0]
            if not current_group:
                break
                
            groups.append(current_group)
            
            for node in current_group:
                del in_degree[node]
                
            for g_id in in_degree.keys():
                in_degree[g_id] = sum(1 for dep in self.goals[g_id].dependencies if dep in in_degree)
                
        return groups

def decompose_goal(high_level_goal: str) -> GoalDAG:
    dag = GoalDAG()
    goal_lower = high_level_goal.lower()
    
    subgoals = []
    if 'login system' in goal_lower:
        subgoals = ['hash passwords', 'add rate limiting', 'JWT tokens', 'email verification', 'account lockout', 'GDPR deletion endpoint']
    elif 'rest api' in goal_lower:
        subgoals = ['add input validation', 'add error handling', 'add OpenAPI docs', 'add authentication', 'add rate limiting', 'add logging']
    elif 'deploy to production' in goal_lower:
        subgoals = ['write Dockerfile', 'add health check', 'create K8s manifests', 'set up CI/CD', 'configure monitoring', 'write runbook']
    else:
        subgoals = ['analyze requirements', 'design architecture', 'implement', 'test', 'deploy']
        
    for i, sg in enumerate(subgoals):
        dag.add_goal(Goal(
            goal_id=f"goal_{i}",
            description=sg,
            dependencies=[],
            success_criteria="Completed successfully",
            estimated_complexity=3
        ))
        
    return dag

def get_execution_plan(dag: GoalDAG) -> List[List[str]]:
    return dag.get_parallel_groups()

def inject_goal_decomposition_prompt(system_prompt: str, task: str = '') -> str:
    directive = (
        f"\n\n[GOAL DECOMPOSITION DIRECTIVE]\n"
        f"Break down the task '{task}' into a DAG of parallelizable sub-goals."
    )
    return system_prompt + directive
