import json

class SkillRegistry:
    """
    yAI Omni-Intelligence Pillar 5: Dynamic Skill Injection.
    Inspired by stitch-skills and agentic-awesome-skills.
    Instead of hardcoding tools into agents, agents query this registry 
    to dynamically discover and inject tools at runtime.
    """
    def __init__(self):
        # Mock database of external skills
        self.skills = {
            "web_search": {
                "name": "duckduckgo_search",
                "description": "Searches the web for latest documentation.",
                "action": "Executes a web search."
            },
            "database_inspector": {
                "name": "pg_dump_inspector",
                "description": "Reads Postgres schema for context.",
                "action": "Connects to DB and dumps schema."
            },
            "security_scanner": {
                "name": "bandit_sec_scan",
                "description": "Runs static application security testing (SAST).",
                "action": "Scans code for vulnerabilities."
            }
        }
        
    def get_available_skills(self) -> str:
        """Returns a JSON string of all available skills for the agent to read."""
        return json.dumps(self.skills, indent=2)
        
    def inject_skill(self, skill_name: str) -> str:
        """Simulates injecting a skill's execution logic into the agent's context."""
        if skill_name in self.skills:
            return f"[Skill Injected] {self.skills[skill_name]['name']} is now available to the Swarm."
        return f"[Skill Error] {skill_name} not found in registry."
