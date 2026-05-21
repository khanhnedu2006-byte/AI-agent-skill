# Đề bài Intern: AI Agent với Skill Registry

## 1. Bối cảnh

Bạn đã bao giờ thấy ChatGPT/Claude có thể làm nhiều việc khác nhau - đọc PDF, tính toán, viết email — nhưng không phải lúc nào cũng load hết khả năng vào đầu? Đó là vì nó có cơ chế **skills**.

**Skill** = một folder chứa file `SKILL.md`, trong đó có:
- **Mô tả ngắn** (khi nào dùng skill này)
- **Hướng dẫn chi tiết** (làm gì khi được kích hoạt)

Agent hoạt động như sau:
1. Lúc khởi động, agent đọc *mô tả ngắn* của tất cả skills (rẻ, nhanh)
2. User gửi câu hỏi → agent dùng LLM xem skill nào phù hợp
3. Chỉ khi đó mới đọc *hướng dẫn chi tiết* của skill được chọn
4. Agent làm theo hướng dẫn, trả lời user

Hãy code lại cơ chế này bằng Python + LangChain. Không cần fancy, chỉ cần chạy đúng.

## 2. Yêu cầu MVP (bắt buộc)

### 2.1. Cấu trúc skill

Tạo folder `skills/`, mỗi skill là 1 subfolder có file `SKILL.md`:

```
skills/
├── calculator/
│   └── SKILL.md
└── weather/
    └── SKILL.md
```

Format của `SKILL.md`:

```markdown
---
name: calculator
description: Use this skill when the user asks to compute math expressions, do arithmetic, or evaluate formulas.
---

# Calculator

When the user asks a math question:
1. Extract the math expression from their query
2. Evaluate it using Python's eval() (safe context only)
3. Return the result in a friendly sentence

Example:
- User: "What's 25 * 4 + 10?"
- You: "25 * 4 + 10 equals 110."
```

### 2.2. Code cần viết

Có 3 class chính:

**`SkillRegistry`** — quản lý skills
```python
class SkillRegistry:
    def __init__(self, skills_dir: str): ...
    def list_skills(self) -> list[dict]:
        # Trả về [{"name": ..., "description": ...}, ...]
        # CHỈ đọc YAML frontmatter, KHÔNG đọc full content
        ...
    def get_skill_content(self, name: str) -> str:
        # Đọc full content của 1 skill khi được chọn
        ...
```

**`SkillSelector`** — chọn skill dựa trên query
```python
class SkillSelector:
    def select(self, query: str, skills: list[dict]) -> str | None:
        # Đưa list (name, description) + query vào LLM
        # LLM trả về tên skill phù hợp, hoặc None nếu không có
        ...
```
> Dùng LLM open-source local qua `langchain_ollama.ChatOllama`. Prompt tự thiết kế.

**`Agent`** — kết nối tất cả
```python
class Agent:
    def run(self, query: str) -> str:
        # 1. Lấy list skills từ registry
        # 2. Dùng selector chọn skill
        # 3. Nếu có skill → load content, đưa vào prompt làm system message
        # 4. Nếu không có skill → trả lời bằng general knowledge
        # 5. Return response
        ...
```

### 2.3. Skills cần làm

Viết **2 skills** hoạt động được:
1. **`calculator`** — tính toán biểu thức số học
2. **`weather`** — trả lời thời tiết (có thể fake data, không cần gọi API thật)

### 2.4. Demo

File `demo.py` chạy 4 query sau và in kết quả:
```python
queries = [
    "What's 15 * 23?",                    # → calculator
    "How's the weather in Hanoi today?",  # → weather
    "Tell me a joke",                     # → no skill, general answer
    "Calculate the area of a circle with radius 5",  # → calculator
]
```

## 3. Deliverables

1. **GitHub repo** với code
2. **README.md** ngắn gọn: cách cài (Ollama + `pip install`), cách pull model, cách chạy demo
3. **3 - 5 skills** ở folder `skills/`
4. **`demo.py`** chạy được
5. **3-5 unit tests** với pytest (test parse YAML, test list_skills, v.v)

## 4. Stack

- Python 3.10+
- `langchain` + `langchain-ollama`
- `pyyaml` để parse frontmatter
- `pytest` để test

**LLM: dùng open-source model qua Ollama (chạy local, miễn phí, không cần API key).**

### Setup Ollama

1. Cài Ollama: https://ollama.com/download (Mac/Linux/Windows đều có)
2. Pull một model. Đề xuất:
   - **`llama3.2:3b`** — nhẹ (~2GB), chạy được trên laptop 8GB RAM, đủ tốt cho bài này
   - **`qwen2.5:7b`** — tốt hơn cho instruction following, cần ~6GB RAM
   - **`mistral:7b`** — 
   ```bash
   ollama pull llama3.2:3b
   ```
3. Test chạy thử:
   ```bash
   ollama run llama3.2:3b "Hello, are you working?"
   ```
4. Trong code, kết nối qua LangChain:
   ```python
   from langchain_ollama import ChatOllama
   llm = ChatOllama(model="llama3.2:3b", temperature=0)
   ```


## 5. Suggested timeline (1 tuần full-time)

| Ngày | Mục tiêu |
|---|---|
| 1 | Cài Ollama, pull model, test chạy được. Đọc tài liệu LangChain (basic Chat models, prompts). Tạo repo, viết `SkillRegistry` + 1 skill mẫu |
| 2 | Viết `SkillSelector` + test với 2-3 query |
| 3 | Viết `Agent` class, ráp tất cả lại, chạy được end-to-end |
| 4 | Hoàn thiện 2 skills, viết demo.py |
| 5 | Viết tests, README, refactor code cho clean |

## 6. Bonus (có thì tốt, không có cũng ok)

Chọn 1 trong các ý sau, KHÔNG cần làm hết:
- Thêm skill thứ 3 phức tạp hơn (ví dụ: đọc file CSV và trả lời câu hỏi về nó)
- Cho phép skill có sub-script Python (skill trỏ tới file `.py`, agent execute file đó)
- Web UI đơn giản với Streamlit

## 7. Câu hỏi để thảo luận với mentor (sau khi xong)

1. Nếu có 50 skills, cách select hiện tại còn ổn không? Tại sao?
2. Sự khác biệt giữa "skill" (trong bài này) và "tool" trong LangChain là gì?
3. Nếu LLM chọn sai skill, làm sao biết được?
4. Có cách nào có thể chọn multiple skills cho cùng 1 task không?