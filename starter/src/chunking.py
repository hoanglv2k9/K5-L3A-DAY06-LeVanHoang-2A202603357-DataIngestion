# -*- coding: utf-8 -*-
"""Implement fixed-size and structure-aware chunking."""
from .models import Chunk, DocumentPage


def fixed_size(page: DocumentPage, size: int = 500, overlap: int = 50) -> list[Chunk]:
    """Strategy A: Split text into overlapping windows and retain page metadata."""
    text = page.text
    if not text:
        return []
    
    chunks: list[Chunk] = []
    start = 0
    chunk_idx = 0
    text_len = len(text)
    
    step = max(1, size - overlap)
    
    while start < text_len:
        end = min(start + size, text_len)
        chunk_text = text[start:end].strip()
        
        if chunk_text:
            chunks.append(
                Chunk(
                    chunk_id=f"{page.document_id}_p{page.page}_c{chunk_idx}",
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=chunk_text,
                    metadata={
                        **page.metadata,
                        "chunking_strategy": "fixed_size",
                        "start_char": start,
                        "end_char": end,
                        "char_count": len(chunk_text)
                    }
                )
            )
            chunk_idx += 1
            
        if end >= text_len:
            break
        start += step
        
    return chunks


def by_paragraph(page: DocumentPage, max_size: int = 800) -> list[Chunk]:
    """Strategy B & C: Structure-aware chunking by heading/paragraph, grouping small units."""
    text = page.text
    if not text:
        return []

    # Chia đoạn theo dòng hoặc heading
    raw_paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not raw_paragraphs:
        raw_paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    chunks: list[Chunk] = []
    current_group: list[str] = []
    current_len = 0
    chunk_idx = 0

    for para in raw_paragraphs:
        para_len = len(para)
        # Nếu đoạn quá dài đơn lẻ, cắt thành các phần vừa vặn
        if para_len > max_size:
            if current_group:
                merged_text = "\n\n".join(current_group)
                chunks.append(
                    Chunk(
                        chunk_id=f"{page.document_id}_p{page.page}_c{chunk_idx}",
                        document_id=page.document_id,
                        source=page.source,
                        page=page.page,
                        text=merged_text,
                        metadata={
                            **page.metadata,
                            "chunking_strategy": "by_paragraph",
                            "char_count": len(merged_text)
                        }
                    )
                )
                chunk_idx += 1
                current_group = []
                current_len = 0
                
            # Cắt đoạn dài thành các chunk max_size
            p_start = 0
            while p_start < para_len:
                p_end = min(p_start + max_size, para_len)
                sub_text = para[p_start:p_end].strip()
                chunks.append(
                    Chunk(
                        chunk_id=f"{page.document_id}_p{page.page}_c{chunk_idx}",
                        document_id=page.document_id,
                        source=page.source,
                        page=page.page,
                        text=sub_text,
                        metadata={
                            **page.metadata,
                            "chunking_strategy": "by_paragraph",
                            "char_count": len(sub_text)
                        }
                    )
                )
                chunk_idx += 1
                p_start = p_end
            continue

        if current_len + para_len + 2 > max_size and current_group:
            merged_text = "\n\n".join(current_group)
            chunks.append(
                Chunk(
                    chunk_id=f"{page.document_id}_p{page.page}_c{chunk_idx}",
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=merged_text,
                    metadata={
                        **page.metadata,
                        "chunking_strategy": "by_paragraph",
                        "char_count": len(merged_text)
                    }
                )
            )
            chunk_idx += 1
            current_group = [para]
            current_len = para_len
        else:
            current_group.append(para)
            current_len += para_len + 2

    if current_group:
        merged_text = "\n\n".join(current_group)
        chunks.append(
            Chunk(
                chunk_id=f"{page.document_id}_p{page.page}_c{chunk_idx}",
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=merged_text,
                metadata={
                    **page.metadata,
                    "chunking_strategy": "by_paragraph",
                    "char_count": len(merged_text)
                }
            )
        )

    return chunks
