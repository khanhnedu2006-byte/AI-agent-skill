import os
import subprocess
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from skill_registry import SkillRegistry
from skill_selector import SkillSelector
from pdf_handler import extract_text_from_pdf

class Agent:
    def __init__(self, skills_dir: str = "skills", model: str = "llama3.2:3b"):
        self.registry = SkillRegistry(skills_dir)
        self.selector = SkillSelector(model)
        self.llm = ChatOllama(model=model, temperature=0)

    def _run_subscript(self, skill_name: str, query: str) -> str | None:
        """Chạy sub-script Python của skill nếu có, trả về output."""
        script_path = os.path.join(self.registry.skills_dir, skill_name, f"{skill_name}.py")
        if not os.path.exists(script_path):
            return None

        # Bước 1: dùng LLM extract expression từ query
        extract_prompt = f"""Extract only the math expression from this query.
Return ONLY the expression, nothing else. No words, no explanation.
Examples:
- "What is 15 * 23?" → 15 * 23
- "Area of circle radius 5" → 3.14159 * 5**2
- "What is 2 to the power of 8?" → 2**8
- "What is (2**10 + 3**5 - 150) / (7 * 4 - 18)?" → (2**10 + 3**5 - 150) / (7 * 4 - 18)

Query: {query}"""

        response = self.llm.invoke([HumanMessage(content=extract_prompt)])
        expression = response.content.strip()

        # Bước 2: chạy script với expression
        result = subprocess.run(
            ["python", script_path, expression],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"[WARNING] Script error: {result.stderr.strip()}")
            return None

        return result.stdout.strip() if result.stdout else None

    def run(self, query: str) -> tuple[str, str | None]:
        """Chạy query, trả về (answer, selected_skill)."""
        skills = self.registry.list_skills()
        selected = self.selector.select(query, skills)

        if selected:
            skill_content = self.registry.get_skill_content(selected)

            # Thử chạy sub-script trước
            script_result = self._run_subscript(selected, query)

            if script_result:
                # Có kết quả từ script → đưa vào prompt
                system_message = f"{skill_content}\n\nScript result: {script_result}"
            else:
                # Không có script → LLM tự xử lý
                system_message = skill_content

            messages = [
                SystemMessage(content=system_message),
                HumanMessage(content=query)
            ]
        else:
            messages = [
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content=query)
            ]

        response = self.llm.invoke(messages)
        return response.content, selected

    def run_with_pdf(self, query: str, pdf_path: str) -> str:
        """Chạy query kèm nội dung PDF extract được."""
        pdf_text = extract_text_from_pdf(pdf_path)
        skill_content = self.registry.get_skill_content("pdf_reader")
        system_message = f"{skill_content}\n\n## PDF Content\n{pdf_text}"
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=query)
        ]
        response = self.llm.invoke(messages)
        return response.content