from agent import Agent
import os

agent = Agent()

def run_query(query: str):
    answer, selected = agent.run(query)
    print(f"Query    : {query}")
    print(f"Skill    : {selected if selected else 'none (general knowledge)'}")
    print(f"Answer   : {answer}")
    print("-" * 60)

def run_pdf_query(query: str, pdf_path: str):
    answer = agent.run_with_pdf(query, pdf_path)
    print(f"Query    : {query}")
    print(f"Skill    : pdf_reader")
    print(f"Answer   : {answer}")
    print("-" * 60)

print("=" * 60)
print("      AI AGENT WITH SKILL REGISTRY - DEMO")
print("=" * 60)
print()

queries = [
    "What is (2**10 + 3**5 - 150) / (7 * 4 - 18)?",
    "How's the weather in Hanoi today?",
    "Tell me a joke",
]

for query in queries:
    run_query(query)

pdf_path = "sample.pdf"
if os.path.exists(pdf_path):
    run_pdf_query("Summarize this PDF file", pdf_path)
else:
    print("(Bỏ qua PDF test — không tìm thấy sample.pdf)")
    print("-" * 60)