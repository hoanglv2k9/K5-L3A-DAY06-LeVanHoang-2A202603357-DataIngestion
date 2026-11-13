# -*- coding: utf-8 -*-
"""Smoke-test script to verify Gemini Embedding + Qdrant Vector Store on 1 page and 1 question."""
import json
import sys
from pathlib import Path

starter_dir = Path(__file__).resolve().parent.parent
if str(starter_dir) not in sys.path:
    sys.path.insert(0, str(starter_dir))

from src.ingestion import load_pdf
from src.chunking import fixed_size, by_paragraph
from src.embeddings import GeminiEmbedder
from src.store import VectorStore
from src.evaluation import evaluate_query


def run_smoke_test():
    print("=" * 60)
    print("CHẠY THỬ SMOKE-TEST (1 TRANG + 1 CÂU HỎI)")
    print("=" * 60)

    pdf_path = starter_dir / "data" / "toan_6_tap_1_va_2_gdpt2018.pdf"
    benchmark_path = starter_dir.parent / "benchmark" / "benchmark_questions.json"

    # 1. Trích xuất trang 1
    print("\n1. Trích xuất trang 1 từ PDF...")
    pages = load_pdf(pdf_path, document_id="toan-6-gdpt2018", source="toan_6_tap_1_va_2_gdpt2018.pdf")
    p1 = pages[0]
    print(f"-> Trang 1: {p1.metadata.get('char_count')} ký tự, Section: {p1.metadata.get('section')}")

    # 2. Chunking
    print("\n2. Thử nghiệm Chunking...")
    chunks_fixed = fixed_size(p1, size=500, overlap=50)
    chunks_para = by_paragraph(p1, max_size=800)
    print(f"-> Fixed size chunks: {len(chunks_fixed)}")
    print(f"-> Paragraph chunks: {len(chunks_para)}")

    # 3. Embed & Vector Store
    print("\n3. Gọi Gemini API Embedding (Model: models/gemini-embedding-001, delay 4s)...")
    embedder = GeminiEmbedder(model_name="models/gemini-embedding-001", delay_seconds=4.0)
    print(f"-> Khởi tạo embedder thành công! Dimensions: {embedder.dimensions}")

    test_db = starter_dir / "results" / "smoke_test_qdrant"
    store = VectorStore(storage_path=str(test_db), dimensions=embedder.dimensions)

    texts = [c.text for c in chunks_para]
    print(f"-> Đang embed {len(texts)} chunks...")
    vectors = embedder.embed_documents(texts)
    store.upsert("smoke_test_col", chunks_para, vectors)
    print("-> Đã lưu vector vào Qdrant thành công!")

    # 4. Query & Search
    print("\n4. Chạy truy vấn với câu hỏi q01...")
    with open(benchmark_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
    q1 = questions[0]
    print(f"-> Câu hỏi: {q1['question']}")
    print(f"-> Gold page: {q1['gold_page']}")

    q_vec = embedder.embed_query(q1["question"])
    hits = store.search("smoke_test_col", q_vec, top_k=3)
    print(f"-> Tìm thấy {len(hits)} kết quả.")

    # 5. Evaluate
    trace = evaluate_query(q1, hits)
    print("\n5. Kết quả đánh giá Smoke-Test:")
    print(f"-> Hit@1: {trace['hit_at_1']}")
    print(f"-> Hit@3: {trace['hit_at_3']}")
    print(f"-> Top 1 Score: {hits[0]['score']:.4f}")
    print(f"-> Top 1 Text snippet: {hits[0]['text'][:120]}...")
    print("=" * 60)
    print("SMOKE-TEST HOÀN TẤT THÀNH CÔNG RỰC RỠ!")
    print("=" * 60)


if __name__ == "__main__":
    run_smoke_test()

