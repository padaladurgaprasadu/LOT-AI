from typing import Dict, List, Any

class SprintPlanner:
    """Agile sprint planning and velocity tracking."""
    
    def create_sprint(self, backlog: List[Dict[str, Any]], capacity_points: int = 40) -> Dict[str, Any]:
        sprint_items = []
        total_points = 0
        overflow = []
        
        # Sort by priority (assuming lower number is higher priority, or just sort by a 'priority' string)
        # Assuming backlog is pre-sorted or we sort here.
        for item in backlog:
            points = item.get("story_points", 0)
            if total_points + points <= capacity_points:
                sprint_items.append(item)
                total_points += points
            else:
                overflow.append(item)
                
        return {"sprint_items": sprint_items, "total_points": total_points, "overflow": overflow}

    def calculate_velocity(self, historical_sprints: List[Dict[str, int]]) -> Dict[str, Any]:
        if not historical_sprints:
            return {"avg_velocity": 0, "trend": "stable", "reliability": 0}
            
        completed = [s.get("completed", 0) for s in historical_sprints]
        avg = sum(completed) / len(completed)
        return {"avg_velocity": avg, "trend": "up" if completed[-1] >= avg else "down", "reliability": 0.85}

    def predict_completion(self, remaining_stories: List[Dict], velocity: float) -> Dict[str, Any]:
        total_points = sum(s.get("story_points", 0) for s in remaining_stories)
        sprints = total_points / velocity if velocity > 0 else float('inf')
        return {"eta_sprints": sprints, "eta_weeks": sprints * 2, "confidence": 0.9}

    def generate_burndown_data(self, sprint_items: List[Dict], start_date: str, end_date: str) -> List[Dict[str, Any]]:
        total = sum(i.get("story_points", 0) for i in sprint_items)
        return [
            {"date": start_date, "remaining": total},
            {"date": end_date, "remaining": 0}
        ]

    def prioritise_backlog(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # WSJF = Value / Effort
        def wsjf(item):
            effort = item.get("effort", 1)
            return item.get("value", 0) / effort if effort > 0 else 0
            
        return sorted(items, key=wsjf, reverse=True)

    def identify_blockers(self, sprint_items: List[Dict]) -> List[str]:
        blockers = []
        for item in sprint_items:
            if "dependency" in item:
                blockers.append(f"{item['title']} is blocked by {item['dependency']}")
        return blockers

def inject_sprint_planner_prompt(system_prompt: str) -> str:
    return system_prompt + "\nUse SprintPlanner to manage agile workflows."
