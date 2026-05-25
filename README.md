# AI Agent with Skill Registry

Một AI Agent chạy hoàn toàn **local** sử dụng cơ chế **Skill Registry** — thay vì load toàn bộ khả năng vào prompt, agent chỉ đọc mô tả ngắn của từng skill, dùng LLM chọn skill phù hợp, rồi mới load hướng dẫn chi tiết. Không cần API key, không tốn phí.

---

## Tính năng

- **Skill Registry** — tự động phát hiện skills mới, không cần sửa code
- **Lazy Loading** — chỉ đọc full content của skill được chọn, tiết kiệm token
- **Sub-script execution** — skill có thể gọi Python script thật để tính toán chính xác 100%
- **PDF Reader** — extract và trả lời câu hỏi về nội dung PDF
- **General fallback** — trả lời bằng general knowledge khi không có skill phù hợp

---

## Skills có sẵn

| Skill | Mô tả | Sub-script |
|---|---|---|
| `calculator` | Tính toán biểu thức số học | ✅ `calculator.py` |
| `weather` | Trả lời thời tiết (fake data) | ❌ |
| `pdf_reader` | Đọc và trả lời câu hỏi về PDF | ✅ `pdf_handler.py` |

---

## Yêu cầu hệ thống

- Python 3.10+
- [Ollama](https://ollama.com/download) (Mac / Linux / Windows)
- RAM tối thiểu 8GB

---

## Cài đặt

### 1. Clone repo

```bash
git clone https://github.com/khanhnedu2006-byte/AI-agent-skill.git
cd AI-agent-skill
```

### 2. Cài Ollama

Tải và cài tại: https://ollama.com/download

Sau khi cài, mở Ollama app để service chạy ngầm, sau đó pull model:

```bash
ollama pull llama3.2:3b
```

> Model nặng ~2GB. Máy yếu RAM < 8GB dùng: `ollama pull llama3.2:1b`

Kiểm tra model sẵn sàng:

```bash
ollama list
```

### 3. Tạo virtual environment

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

### 4. Cài dependencies

```bash
pip install -r requirements.txt
```

---

## Chạy demo

```bash
python demo.py
```

Output mẫu:

```
============================================================
      AI AGENT WITH SKILL REGISTRY - DEMO
============================================================

Query    : What's 15 * 23?
Skill    : calculator
Answer   : 15 * 23 equals 345.
------------------------------------------------------------
Query    : What is (2**10 + 3**5 - 150) / (7 * 4 - 18)?
Skill    : calculator
Answer   : The result is 111.7.
------------------------------------------------------------
Query    : How's the weather in Hanoi today?
Skill    : weather
Answer   : It's currently 32°C and sunny in Hanoi. Stay hydrated!
------------------------------------------------------------
Query    : Tell me a joke
Skill    : none (general knowledge)
Answer   : Why don't scientists trust atoms? Because they make up everything!
------------------------------------------------------------
Query    : Calculate the area of a circle with radius 5
Skill    : calculator
Answer   : The area of a circle with radius 5 is approximately 78.54.
------------------------------------------------------------
```

---

## Cấu trúc project

```
AI-agent-skill/
├── skills/
│   ├── calculator/
│   │   ├── SKILL.md          # Hướng dẫn LLM tính toán
│   │   └── calculator.py     # Script tính toán chính xác (safe eval)
│   ├── weather/
│   │   └── SKILL.md          # Hướng dẫn trả lời thời tiết
│   └── pdf_reader/
│       └── SKILL.md          # Hướng dẫn đọc và trả lời về PDF
├── tests/
│   ├── __init__.py
│   └── test_registry.py      # 7 unit tests
├── skill_registry.py         # Quản lý và load skills
├── skill_selector.py         # Dùng LLM chọn skill phù hợp
├── agent.py                  # Kết nối tất cả, xử lý query
├── pdf_handler.py            # Extract text từ PDF (pymupdf)
├── demo.py                   # Chạy các query mẫu
├── requirements.txt
└── README.md
```

---

## Chạy tests

```bash
pytest tests/ -v
```

Kết quả mong đợi:

```
tests/test_registry.py::test_list_skills_returns_list              PASSED
tests/test_registry.py::test_list_skills_correct_count             PASSED
tests/test_registry.py::test_list_skills_has_name_and_description  PASSED
tests/test_registry.py::test_list_skills_correct_values            PASSED
tests/test_registry.py::test_get_skill_content_returns_string      PASSED
tests/test_registry.py::test_get_skill_content_has_frontmatter     PASSED
tests/test_registry.py::test_get_skill_content_not_found           PASSED

7 passed in 0.12s
```

---

## Cách hoạt động

```
User query
    ↓
SkillRegistry.list_skills()       # Đọc mô tả ngắn tất cả skills (lazy load)
    ↓
SkillSelector.select()            # LLM chọn skill phù hợp (hoặc none)
    ↓
  ┌─────────────────────────────────────┐
  │ Có skill                            │ Không có skill
  ↓                                     ↓
_run_subscript()                   General knowledge
  ↓
  ┌──────────────────────────────┐
  │ Có sub-script (.py)          │ Không có sub-script
  ↓                              ↓
Python chạy code thật       LLM tự xử lý
(chính xác 100%)            dựa trên SKILL.md
  └──────────────────────────────┘
    ↓
Agent trả lời user
```

---

## Thêm skill mới

1. Tạo folder mới trong `skills/`:

```bash
mkdir skills/ten-skill-moi
```

2. Tạo `skills/ten-skill-moi/SKILL.md` theo format:

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

3. (Tuỳ chọn) Thêm sub-script `skills/ten-skill-moi/ten-skill-moi.py` nếu cần chạy code thật.

Agent tự động nhận diện skill mới, **không cần sửa code**.

---

## Bonus đã implement

- ✅ **Sub-script execution** — `calculator` dùng `safe_eval()` thay vì để LLM tự tính, đảm bảo chính xác với phép tính phức tạp
- ✅ **PDF Reader** — dùng `pymupdf` extract text giữ nguyên cấu trúc trang

---

## Stack

| Thành phần | Công nghệ |
|---|---|
| LLM runtime | [Ollama](https://ollama.com) |
| Model | `llama3.2:3b` |
| LLM framework | LangChain + langchain-ollama |
| YAML parsing | PyYAML |
| PDF extraction | PyMuPDF (fitz) |
| Testing | pytest |