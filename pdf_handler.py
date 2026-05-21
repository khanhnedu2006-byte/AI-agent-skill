import fitz  # pymupdf

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract toàn bộ text từ PDF, giữ nguyên cấu trúc trang."""
    doc = fitz.open(pdf_path)
    full_text = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")  # giữ layout tốt nhất
        if text.strip():
            full_text.append(f"--- Page {page_num} ---\n{text}")

    doc.close()
    return "\n\n".join(full_text)