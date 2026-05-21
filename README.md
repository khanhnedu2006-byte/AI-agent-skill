# AI-agent-skill
AI Agent with Skill Registry — LangChain + Ollama
# AI Agent with Skill Registry

Một AI Agent đơn giản sử dụng cơ chế **Skill Registry** — thay vì load toàn bộ khả năng vào prompt, agent chỉ đọc mô tả ngắn của từng skill, dùng LLM chọn skill phù hợp, rồi mới load hướng dẫn chi tiết. Chạy hoàn toàn local, không cần API key.

---

## Yêu cầu hệ thống

- Python 3.10+
- [Ollama](https://ollama.com/download) (để chạy LLM local)

---

## Cài đặt

### 1. Clone repo

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Cài Ollama

Tải và cài tại: https://ollama.com/download (hỗ trợ Mac, Linux, Windows)

Sau khi cài, mở Ollama app để service chạy ngầm.

### 3. Pull model

```bash
ollama pull llama3.2:3b
```

> Model nặng ~2GB, chờ vài phút. Yêu cầu tối thiểu 8GB RAM.  
> Máy yếu hơn dùng: `ollama pull llama3.2:1b`

Kiểm tra model đã sẵn sàng:

```bash
ollama list
```

### 4. Tạo virtual environment

```bash
python -m venv venv
```

Kích hoạt:

```bash
# Mac/Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\activate
```

### 5. Cài dependencies

```bash
pip install -r requirements.txt
```

---

## Chạy demo

```bash
python demo.py
```

Demo sẽ chạy 4 câu hỏi mẫu và in ra skill được chọn cùng câu trả lời:

```
Query: What's 15 * 23?
Skill selected: calculator
Answer: 15 * 23 equals 345.

Query: How's the weather in Hanoi today?
Skill selected: weather
Answer: It's currently 32°C and sunny in Hanoi.

Query: Tell me a joke
Skill selected: none
Answer: Why don't scientists trust atoms? Because they make up everything!

Query: Calculate the area of a circle with radius 5
Skill selected: calculator
Answer: The area of a circle with radius 5 is approximately 78.54.
```

---

## Cấu trúc project

```
AI-agent-skill/
├── skills/
│   ├── calculator/
│   │   └── SKILL.md       # Skill tính toán số học
│   └── weather/
│       └── SKILL.md       # Skill trả lời thời tiết
├── tests/
│   ├── __init__.py
│   └── test_registry.py   # Unit tests
├── skill_registry.py      # Quản lý và load skills
├── skill_selector.py      # Dùng LLM chọn skill phù hợp
├── agent.py               # Kết nối tất cả, xử lý query
├── demo.py                # Chạy các câu hỏi mẫu
├── requirements.txt
└── README.md
```

---

## Chạy tests

```bash
pytest tests/ -v
```

---

## Cách hoạt động

```
User query
    ↓
SkillRegistry.list_skills()     # Đọc mô tả ngắn tất cả skills
    ↓
SkillSelector.select()          # LLM chọn skill phù hợp (hoặc none)
    ↓
SkillRegistry.get_skill_content()   # Load hướng dẫn chi tiết của skill được chọn
    ↓
Agent trả lời dựa trên hướng dẫn đó
```

---

## Thêm skill mới

1. Tạo folder mới trong `skills/`:

```bash
mkdir skills/ten-skill-moi
```

2. Tạo file `skills/ten-skill-moi/SKILL.md` theo format:

```markdown
---
name: ten-skill-moi
description: Mô tả ngắn — khi nào dùng skill này (1-2 câu).
---

# Tên Skill

Hướng dẫn chi tiết cho LLM:
1. Bước 1
2. Bước 2

## Examples
- User: "..." → "..."
```

Agent sẽ tự động nhận diện skill mới mà không cần sửa code.

---

## Stack

| Thành phần | Công nghệ |
|---|---|
| LLM runtime | [Ollama](https://ollama.com) |
| Model mặc định | `llama3.2:3b` |
| LLM framework | LangChain + langchain-ollama |
| YAML parsing | PyYAML |
| Testing | pytest |