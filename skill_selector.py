from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

class SkillSelector:
    def __init__(self, model: str = "llama3.2:3b"):
        self.llm = ChatOllama(model=model, temperature=0)

    def select(self, query: str, skills: list[dict]) -> str | None:
        if not skills:
            return None

        # Tạo danh sách skills để đưa vào prompt
        skill_list = "\n".join(
            f"- {s['name']}: {s['description']}" for s in skills
        )

        system_prompt = f"""You are a skill router. Your job is to select the most appropriate skill for a user query.

Available skills:
{skill_list}

Rules:
- Reply with ONLY the exact skill name (e.g: calculator)
- If the query does not clearly match any skill, reply with exactly: none
- Do NOT guess or pick the closest skill if it does not match
- Do NOT explain, do NOT add punctuation, do NOT add anything else

Examples of when to reply "none":
- "Tell me a joke" → none
- "Who is the president?" → none
- "What's the capital of France?" → none"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]

        response = self.llm.invoke(messages)
        result = response.content.strip().lower()

        # Kiểm tra result có đúng tên skill không
        valid_names = {s["name"] for s in skills}
        if result in valid_names:
            return result
        return None