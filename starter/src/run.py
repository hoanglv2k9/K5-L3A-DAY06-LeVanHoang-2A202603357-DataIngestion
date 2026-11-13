# -*- coding: utf-8 -*-
"""Full pipeline execution for Day 06 Data Ingestion lab."""
import csv
import json
import os
import sys
import time
from pathlib import Path

# Thêm đường dẫn starter vào sys.path nếu cần
current_dir = Path(__file__).resolve().parent
starter_dir = current_dir.parent
if str(starter_dir) not in sys.path:
    sys.path.insert(0, str(starter_dir))

from src.ingestion import load_pdf
from src.chunking import fixed_size, by_paragraph
from src.embeddings import GeminiEmbedder
from src.store import VectorStore
from src.evaluation import evaluate_query, summarize


def main() -> None:
    print("=" * 60)
    print("DAY 06: DATA INGESTION ENGINEERING PIPELINE")
    print("Học viên: Lê Văn Hoàng - MSSV: 2A202603357 - Lớp: L3A")
    print("=" * 60)

    base_dir = starter_dir.parent
    data_dir = starter_dir / "data"
    results_dir = starter_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = data_dir / "toan_6_tap_1_va_2_gdpt2018.pdf"
    benchmark_path = base_dir / "benchmark" / "benchmark_questions.json"

    # 1. Tải và kiểm tra tài liệu
    print("\n[Bước 1/5] Đang nạp và trích xuất PDF...")
    pages = load_pdf(pdf_path, document_id="toan-6-gdpt2018", source="toan_6_tap_1_va_2_gdpt2018.pdf")
    print(f"-> Đã trích xuất {len(pages)} trang nội dung.")
    if len(pages) < 30:
        raise ValueError(f"Tài liệu không đạt tối thiểu 30 trang (hiện có: {len(pages)})!")

    # 2. Xây dựng 3 chiến lược chunking
    print("\n[Bước 2/5] Đang tạo chunk theo 3 chiến lược...")
    
    # Strategy A: Fixed-size (500 chars, 50 overlap)
    chunks_A = []
    for p in pages:
        chunks_A.extend(fixed_size(p, size=500, overlap=50))
    print(f"-> Strategy A (Fixed 500 chars, overlap 50): {len(chunks_A)} chunks.")

    # Strategy B: Structured by paragraph/heading (max 800 chars)
    chunks_B = []
    for p in pages:
        chunks_B.extend(by_paragraph(p, max_size=800))
    print(f"-> Strategy B (Structure-aware by paragraph): {len(chunks_B)} chunks.")

    # Strategy C: Cùng chunk như Strategy B, khác biệt duy nhất là dùng metadata filter khi query
    chunks_C = chunks_B
    print(f"-> Strategy C (Structure-aware + Metadata Filter): {len(chunks_C)} chunks.")

    # 3. Khởi tạo Embedder và Vector Store
    print("\n[Bước 3/5] Khởi tạo Gemini Embedder (độ trễ 4.0s/lần gọi) và Vector Store...")
    embedder = GeminiEmbedder(model_name="models/gemini-embedding-001", delay_seconds=4.0)
    db_path = str(results_dir / "qdrant_db")
    store = VectorStore(storage_path=db_path, dimensions=embedder.dimensions)

    print("-> Đang tạo embedding và lưu trữ cho Strategy A...")
    t0_a = time.time()
    texts_A = [c.text for c in chunks_A]
    vectors_A = embedder.embed_documents(texts_A)
    store.upsert("strategy_A", chunks_A, vectors_A)
    time_A = round(time.time() - t0_a, 2)
    print(f"-> Đã lưu Strategy A ({len(chunks_A)} chunks, {time_A}s)")

    print("-> Đang tạo embedding và lưu trữ cho Strategy B...")
    t0_b = time.time()
    texts_B = [c.text for c in chunks_B]
    vectors_B = embedder.embed_documents(texts_B)
    store.upsert("strategy_B", chunks_B, vectors_B)
    time_B = round(time.time() - t0_b, 2)
    print(f"-> Đã lưu Strategy B ({len(chunks_B)} chunks, {time_B}s)")

    # Strategy C dùng chung vector store với Strategy B (vì cùng chunk và embedding)
    time_C = time_B

    # 4. Tải bộ Benchmark và Chạy Retrieval cho cả 3 chiến lược
    print("\n[Bước 4/5] Đang chạy Benchmark Retrieval trên 20 câu hỏi...")
    with open(benchmark_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
    print(f"-> Bộ benchmark: {len(questions)} câu hỏi.")

    # Embed tất cả các câu hỏi
    query_vectors = {}
    print("-> Đang embed câu hỏi benchmark...")
    for q in questions:
        q_id = q["id"]
        query_vectors[q_id] = embedder.embed_query(q["question"])
        time.sleep(0.1)

    all_traces = {"A": [], "B": [], "C": []}

    print("-> Đang thực thi truy xuất top-3 cho Strategy A, B, C...")
    for q in questions:
        q_id = q["id"]
        q_vec = query_vectors[q_id]
        flt = q.get("filter")

        # Strategy A: Không filter
        hits_A = store.search("strategy_A", q_vec, top_k=3, filters=None)
        trace_A = evaluate_query(q, hits_A)
        all_traces["A"].append(trace_A)

        # Strategy B: Không filter
        hits_B = store.search("strategy_B", q_vec, top_k=3, filters=None)
        trace_B = evaluate_query(q, hits_B)
        all_traces["B"].append(trace_B)

        # Strategy C: Áp dụng metadata filter nếu câu hỏi có điều kiện lọc
        hits_C = store.search("strategy_B", q_vec, top_k=3, filters=flt)
        trace_C = evaluate_query(q, hits_C)
        all_traces["C"].append(trace_C)

    # 5. Tổng hợp kết quả và xuất báo cáo
    print("\n[Bước 5/5] Đang tổng hợp số liệu và xuất Artifacts...")
    summaries = {
        "A": summarize(all_traces["A"]),
        "B": summarize(all_traces["B"]),
        "C": summarize(all_traces["C"])
    }

    # Lưu trace và summary
    traces_path = results_dir / "traces.json"
    with open(traces_path, "w", encoding="utf-8") as f:
        json.dump(all_traces, f, ensure_ascii=False, indent=2)

    summary_path = results_dir / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)

    print(f"-> Lưu chi tiết trace: {traces_path}")
    print(f"-> Lưu tóm tắt: {summary_path}")

    # Cập nhật artifacts/experiment_log.csv
    exp_log_path = base_dir / "artifacts" / "experiment_log.csv"
    with open(exp_log_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "strategy", "chunking", "chunk_size", "overlap", "metadata", "filter",
            "vectorizer", "hypothesis", "dev_hit1", "dev_hit3", "test_hit1", "test_hit3", "notes"
        ])
        
        # Row A
        sum_A = summaries["A"]
        writer.writerow([
            "A", "fixed_size", "500", "50", "source,page,section", "none",
            "models/text-embedding-004", "Baseline: Cửa sổ cố định 500 ký tự cắt ngang ý nghĩa",
            sum_A["dev"]["hit1_ratio"], sum_A["dev"]["hit3_ratio"],
            sum_A["test"]["hit1_ratio"], sum_A["test"]["hit3_ratio"],
            f"{len(chunks_A)} chunks, {time_A}s"
        ])
        
        # Row B
        sum_B = summaries["B"]
        writer.writerow([
            "B", "by_paragraph", "800", "0", "source,page,section", "none",
            "models/text-embedding-004", "Semantic: Giữ trọn cấu trúc đề mục heading toán học",
            sum_B["dev"]["hit1_ratio"], sum_B["dev"]["hit3_ratio"],
            sum_B["test"]["hit1_ratio"], sum_B["test"]["hit3_ratio"],
            f"{len(chunks_B)} chunks, {time_B}s"
        ])

        # Row C
        sum_C = summaries["C"]
        writer.writerow([
            "C", "by_paragraph", "800", "0", "source,page,section", "section_filter",
            "models/text-embedding-004", "Metadata Filtering: Giảm nhiễu giữa các chương toán",
            sum_C["dev"]["hit1_ratio"], sum_C["dev"]["hit3_ratio"],
            sum_C["test"]["hit1_ratio"], sum_C["test"]["hit3_ratio"],
            f"{len(chunks_C)} chunks, cùng index B"
        ])

    print("\n" + "=" * 60)
    print("KẾT QUẢ THỬ NGHIỆM:")
    for st in ["A", "B", "C"]:
        s = summaries[st]
        print(f"Strategy {st}:")
        print(f"  Dev  - Hit@1: {s['dev']['hit1_ratio']} ({s['dev']['hit1_pct']}%), Hit@3: {s['dev']['hit3_ratio']} ({s['dev']['hit3_pct']}%)")
        print(f"  Test - Hit@1: {s['test']['hit1_ratio']} ({s['test']['hit1_pct']}%), Hit@3: {s['test']['hit3_ratio']} ({s['test']['hit3_pct']}%)")
    print("=" * 60)
    print("Hoàn thành pipeline thành công!")


if __name__ == "__main__":
    main()
