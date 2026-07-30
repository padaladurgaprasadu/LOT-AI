import uuid
from typing import List, Dict, Optional, Set

class SubGoal:
    def __init__(self, title: str, description: str, preconditions: List[str] = None, expected_output: str = "", success_criteria: str = "", assigned_agent: str = "default", estimated_minutes: int = 0):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.preconditions = preconditions or []
        self.expected_output = expected_output
        self.success_criteria = success_criteria
        self.assigned_agent = assigned_agent
        self.estimated_minutes = estimated_minutes

class DAG:
    def __init__(self):
        self.nodes: Dict[str, SubGoal] = {}

    def add_node(self, node: SubGoal):
        self.nodes[node.id] = node

class GoalDecompositionEngine:
    
    def decompose(self, goal: str) -> DAG:
        dag = DAG()
        goal_lower = goal.lower()
        
        if "login" in goal_lower:
            tasks = ["auth", "password hashing", "JWT", "rate limiting", "email verification", "account lockout", "GDPR deletion endpoint"]
        elif "rest api" in goal_lower:
            tasks = ["models", "routes", "validation", "auth middleware", "error handling", "pagination", "tests", "docs", "docker"]
        elif "deploy" in goal_lower:
            tasks = ["dockerize", "CI/CD", "env secrets", "health check", "monitoring", "rollback plan"]
        else:
            tasks = ["analyze requirement", "implement", "test"]

        prev_id = None
        for t in tasks:
            sg = SubGoal(title=t, description=f"Implement {t}")
            if prev_id:
                sg.preconditions.append(prev_id)
            dag.add_node(sg)
            prev_id = sg.id
            
        if self._has_cycle(dag):
            raise ValueError("Cycle detected in goal decomposition")
            
        return dag

    def _has_cycle(self, dag: DAG) -> bool:
        visited = set()
        rec_stack = set()
        
        def dfs(node_id):
            visited.add(node_id)
            rec_stack.add(node_id)
            
            node = dag.nodes.get(node_id)
            if node:
                for pre in node.preconditions:
                    if pre not in visited:
                        if dfs(pre):
                            return True
                    elif pre in rec_stack:
                        return True
            rec_stack.remove(node_id)
            return False

        for node_id in dag.nodes:
            if node_id not in visited:
                if dfs(node_id):
                    return True
        return False

    def get_execution_order(self, dag: DAG) -> List[SubGoal]:
        # Topological sort
        in_degree = {n_id: 0 for n_id in dag.nodes}
        for node in dag.nodes.values():
            for pre in node.preconditions:
                if pre in in_degree:
                    in_degree[node.id] += 1
                    
        queue = [n_id for n_id, deg in in_degree.items() if deg == 0]
        order = []
        
        while queue:
            curr = queue.pop(0)
            order.append(dag.nodes[curr])
            for node in dag.nodes.values():
                if curr in node.preconditions:
                    in_degree[node.id] -= 1
                    if in_degree[node.id] == 0:
                        queue.append(node.id)
        return order

    def get_parallel_groups(self, dag: DAG) -> List[List[SubGoal]]:
        in_degree = {n_id: 0 for n_id in dag.nodes}
        for node in dag.nodes.values():
            for pre in node.preconditions:
                if pre in in_degree:
                    in_degree[node.id] += 1
                    
        queue = [n_id for n_id, deg in in_degree.items() if deg == 0]
        groups = []
        
        while queue:
            group = [dag.nodes[n_id] for n_id in queue]
            groups.append(group)
            
            next_queue = []
            for curr in queue:
                for node in dag.nodes.values():
                    if curr in node.preconditions:
                        in_degree[node.id] -= 1
                        if in_degree[node.id] == 0:
                            next_queue.append(node.id)
            queue = next_queue
            
        return groups

def inject_goal_decomposition_prompt(system_prompt: str, task: str) -> str:
    return system_prompt + "\\n[GOAL DECOMPOSITION] Break tasks into independent, parallelizable sub-goals.\\n"
