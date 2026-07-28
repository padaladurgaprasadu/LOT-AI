import os
import glob
import yaml

class SkillRegistry:
    def __init__(self, skills_dir="backend/skills"):
        self.skills_dir = skills_dir
        self.skills = []
        self._load_skills()
        
    def _load_skills(self):
        """Scans the skills directory for MCP-style .md files and parses them."""
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir, exist_ok=True)
            
        md_files = glob.glob(os.path.join(self.skills_dir, "*.md"))
        for filepath in md_files:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # Basic frontmatter parsing (very naive for MVP)
                if content.startswith("---"):
                    parts = content.split("---")
                    if len(parts) >= 3:
                        frontmatter_raw = parts[1]
                        body = "---".join(parts[2:]).strip()
                        meta = yaml.safe_load(frontmatter_raw)
                        
                        if meta and "name" in meta:
                            self.skills.append({
                                "name": meta.get("name"),
                                "description": meta.get("description", ""),
                                "body": body
                            })
            except Exception as e:
                print(f"[SkillRegistry] Failed to parse {filepath}: {e}")
                
    async def get_skills_for_task(self, task_description: str) -> str:
        """
        Returns a formatted string of available skills and their usage instructions.
        In a full implementation, this would do semantic similarity search.
        For now, it returns all loaded skills.
        """
        if not self.skills:
            return "No external MCP skills available."
            
        skill_context = "Available External Skills (MCP Protocol):\n\n"
        for skill in self.skills:
            skill_context += f"### Skill: {skill['name']}\n"
            skill_context += f"Description: {skill['description']}\n"
            skill_context += f"Execution Payload:\n{skill['body']}\n\n"
            
        return skill_context
