# -*- coding: utf-8 -*-
"""Read and normalize source data."""
import json
import re
import unicodedata
from pathlib import Path
import pypdf

from .models import DocumentPage


def normalize_text(text: str) -> str:
    """Normalize Unicode to NFC, normalize whitespace while retaining headings and structure."""
    if not text:
        return ""
    # Chuẩn hóa Unicode NFC
    text = unicodedata.normalize("NFC", text)
    # Chuẩn hóa khoảng trắng nhưng giữ ngắt dòng
    lines = []
    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def load_pdf(path: Path, document_id: str, source: str) -> list[DocumentPage]:
    """Extract each physical page; keep page number, text, and section metadata."""
    reader = pypdf.PdfReader(str(path))
    pages: list[DocumentPage] = []
    
    # Đọc manifest nếu có để ánh xạ section cho từng trang
    manifest_path = path.parent / "manifest.json"
    page_to_section = {}
    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
                sections = manifest.get("sections", {})
                for sec_name, sec_info in sections.items():
                    for p_num in sec_info.get("pages", []):
                        page_to_section[p_num] = sec_name
        except Exception:
            pass

    for idx, page in enumerate(reader.pages):
        page_num = idx + 1
        raw_text = page.extract_text() or ""
        clean_text = normalize_text(raw_text)
        
        # Nếu trang rỗng, ghi log cảnh báo
        if not clean_text:
            print(f"[Cảnh báo] Trang {page_num} không có văn bản trích xuất được.")
            
        section = page_to_section.get(page_num, "chung")
        pages.append(
            DocumentPage(
                document_id=document_id,
                source=source,
                page=page_num,
                text=clean_text,
                metadata={
                    "section": section,
                    "char_count": len(clean_text)
                }
            )
        )
    return pages
