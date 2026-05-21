import os
import yaml

class SkillRegistry:
    def __init__(self, skills_dir: str):
        self.skills_dir = skills_dir

    def list_skills(self) -> list[dict]:
        skills = []
        for name in os.listdir(self.skills_dir):
            path = os.path.join(self.skills_dir, name, "SKILL.md")
            if not os.path.exists(path):
                continue
            with open(path, "r") as f:
                content = f.read()
            if content.startswith("---"):
                parts = content.split("---", 2)
                meta = yaml.safe_load(parts[1])
                skills.append({
                    "name": meta["name"],
                    "description": meta["description"]
                })
        return skills

    def get_skill_content(self, name: str) -> str:
        path = os.path.join(self.skills_dir, name, "SKILL.md")
        with open(path, "r") as f:
            return f.read()