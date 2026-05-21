from agent import Agent
from skill_registry import SkillRegistry
from skill_selector import SkillSelector
import os

registry = SkillRegistry("skills")
selector = SkillSelector()
agent = Agent()

def run_query(query: str):
    skills = registry.list_skills()
    selected = selector.select(query, skills)
    answer = agent.run(query)
    print(f"Query    : {query}")
    print(f"Skill    : {selected if selected else 'none (general knowledge)'}")
    print(f"Answer   : {answer}")
    print("-" * 60)

def run_pdf_query(query: str, pdf_path: str):
    skills = registry.list_skills()
    selected = selector.select(query, skills)
    answer = agent.run_with_pdf(query, pdf_path)
    print(f"Query    : {query}")
    print(f"Skill    : {selected if selected else 'none (general knowledge)'}")
    print(f"Answer   : {answer}")
    print("-" * 60)

print("=" * 60)
print("           AI AGENT WITH SKILL REGISTRY - DEMO")
print("=" * 60)
print()

# --- Standard queries ---
queries = [
    "What's 15 * 23?",
    "How's the weather in Hanoi today?",
    "Tell me a joke",
    "Calculate the area of a circle with radius 5",
]

for query in queries:
    run_query(query)

# --- PDF query ---
pdf_path = "sample.pdf"
if os.path.exists(pdf_path):
    run_pdf_query("Summarize this PDF file", pdf_path)
else:
    print("(Bỏ qua PDF test — không tìm thấy sample.pdf)")
    print("-" * 60)