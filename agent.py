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

    def run(self, query: str) -> str:
        skills = self.registry.list_skills()
        selected = self.selector.select(query, skills)

        if selected:
            skill_content = self.registry.get_skill_content(selected)
            messages = [
                SystemMessage(content=skill_content),
                HumanMessage(content=query)
            ]
        else:
            messages = [
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content=query)
            ]

        response = self.llm.invoke(messages)
        return response.content

    def run_with_pdf(self, query: str, pdf_path: str) -> str:
        """Chạy query kèm nội dung PDF extract được."""
        # Extract text từ PDF
        pdf_text = extract_text_from_pdf(pdf_path)

        # Lấy skill content
        skill_content = self.registry.get_skill_content("pdf_reader")

        # Ghép PDF content vào system message
        system_message = f"{skill_content}\n\n## PDF Content\n{pdf_text}"

        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=query)
        ]

        response = self.llm.invoke(messages)
        return response.content