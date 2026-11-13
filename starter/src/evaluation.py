# -*- coding: utf-8 -*-
"""Evaluation and retrieval accuracy metrics (Hit@1, Hit@3) with trace preservation."""
import re
from typing import Any


def _is_evidence_present(evidence_quote: str, chunk_text: str) -> bool:
    """Check if evidence quote or significant part of it exists in chunk text."""
    if not evidence_quote or not chunk_text:
        return False
    # Chuẩn hóa xâu để so sánh bỏ qua ký tự khoảng trắng thừa
    def clean(s: str) -> str:
        s = s.lower()
        s = re.sub(r"[\s\.,;:!?\(\)\[\]\{\}\'\"\\/]+", " ", s)
        return s.strip()

    c_ev = clean(evidence_quote)
    c_chunk = clean(chunk_text)

    # 1. Trùng khớp trực tiếp
    if c_ev in c_chunk:
        return True

    # 2. Hoặc trùng khớp ít nhất 70% các cụm từ quan trọng của evidence
    ev_words = [w for w in c_ev.split() if len(w) > 2]
    if not ev_words:
        return False
    matched = sum(1 for w in ev_words if w in c_chunk)
    return (matched / len(ev_words)) >= 0.75


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    """Check whether retrieved top-k hits contain gold page and gold evidence."""
    gold_page = question.get("gold_page")
    evidence_quote = question.get("evidence_quote", "")
    gold_source_id = question.get("gold_source_id", "")

    hit_details = []
    has_hit_at_1 = False
    has_hit_at_3 = False

    for rank, hit in enumerate(hits):
        hit_page = hit.get("page")
        hit_text = hit.get("text", "")
        hit_source = hit.get("document_id", "")

        is_page_match = (hit_page == gold_page)
        is_evidence_hit = _is_evidence_present(evidence_quote, hit_text)

        is_hit = is_page_match and is_evidence_hit

        hit_details.append({
            "rank": rank + 1,
            "chunk_id": hit.get("chunk_id"),
            "score": hit.get("score"),
            "page": hit_page,
            "is_page_match": is_page_match,
            "is_evidence_hit": is_evidence_hit,
            "is_hit": is_hit,
            "text_snippet": hit_text[:160] + "..." if len(hit_text) > 160 else hit_text,
            "metadata": hit.get("metadata", {})
        })

        if is_hit:
            if rank == 0:
                has_hit_at_1 = True
            has_hit_at_3 = True

    return {
        "question_id": question.get("id"),
        "question": question.get("question"),
        "split": question.get("split"),
        "type": question.get("type"),
        "gold_page": gold_page,
        "gold_evidence": evidence_quote,
        "filter": question.get("filter"),
        "hit_at_1": has_hit_at_1,
        "hit_at_3": has_hit_at_3,
        "hits": hit_details
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate Hit@1 and Evidence Hit@3 by split (dev / test)."""
    splits = {"dev": [], "test": []}
    for t in traces:
        sp = t.get("split", "dev")
        if sp in splits:
            splits[sp].append(t)

    summary = {}
    for sp_name, items in splits.items():
        total = len(items)
        if total == 0:
            summary[sp_name] = {
                "total": 0,
                "hit1_count": 0,
                "hit1_ratio": "0/0",
                "hit1_pct": 0.0,
                "hit3_count": 0,
                "hit3_ratio": "0/0",
                "hit3_pct": 0.0
            }
            continue

        hit1_count = sum(1 for x in items if x.get("hit_at_1", False))
        hit3_count = sum(1 for x in items if x.get("hit_at_3", False))

        summary[sp_name] = {
            "total": total,
            "hit1_count": hit1_count,
            "hit1_ratio": f"{hit1_count}/{total}",
            "hit1_pct": round(hit1_count / total * 100, 1),
            "hit3_count": hit3_count,
            "hit3_ratio": f"{hit3_count}/{total}",
            "hit3_pct": round(hit3_count / total * 100, 1)
        }

    return summary
