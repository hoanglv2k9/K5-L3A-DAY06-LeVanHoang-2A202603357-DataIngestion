# -*- coding: utf-8 -*-
"""Generate audit labels and manual evaluation records for Day 06 Report."""
import json
import os

base_dir = r"c:\Users\Student\Documents\aivin\K5-L3A-DAY06-LeVanHoang-2A202603357-DataIngestion"
results_dir = os.path.join(base_dir, "starter", "results")

# 1. 10 Sample Positions for Chunk Coherence (Trang 1 - 10)
COHERENCE_SAMPLES = [
    {
        "position": 1,
        "page": 1,
        "title": "Tập hợp số tự nhiên",
        "scores": {
            "A": {"score": 1, "reason": "Cửa sổ 500 ký tự cắt ngang giữa phần giới thiệu N* và tính chất liền trước, liền sau."},
            "B": {"score": 2, "reason": "Giữ trọn vẹn toàn bộ mục 1 (Khái niệm tập hợp) và mục 2 (Tập hợp N)."},
            "C": {"score": 2, "reason": "Giống B, cấu trúc đoạn giữ trọn ý nghĩa toán học."}
        }
    },
    {
        "position": 2,
        "page": 2,
        "title": "Ghi số tự nhiên & La Mã",
        "scores": {
            "A": {"score": 1, "reason": "Bị cắt giữa phần các chữ số La Mã cơ bản và quy tắc trừ IV, IX."},
            "B": {"score": 2, "reason": "Mỗi đề mục chữ số La Mã và Hệ thập phân nằm trọn trong 1 chunk."},
            "C": {"score": 2, "reason": "Giống B, đầy đủ ngữ cảnh."}
        }
    },
    {
        "position": 3,
        "page": 3,
        "title": "Phép tính & Luỹ thừa",
        "scores": {
            "A": {"score": 1, "reason": "Công thức chia hai luỹ thừa cùng cơ số bị tách khỏi điều kiện a khác 0 và m >= n."},
            "B": {"score": 2, "reason": "Công thức và điều kiện đi kèm nguyên vẹn."},
            "C": {"score": 2, "reason": "Giống B, trọn vẹn công thức."}
        }
    },
    {
        "position": 4,
        "page": 4,
        "title": "Thứ tự thực hiện phép tính",
        "scores": {
            "A": {"score": 2, "reason": "Đoạn quy tắc ngoặc tròn, vuông, nhọn vừa vặn nằm trong 500 ký tự."},
            "B": {"score": 2, "reason": "Giữ trọn vẹn hai mục biểu thức có ngoặc và không có ngoặc."},
            "C": {"score": 2, "reason": "Giống B."}
        }
    },
    {
        "position": 5,
        "page": 5,
        "title": "Tính chất chia hết & Dấu hiệu",
        "scores": {
            "A": {"score": 1, "reason": "Dấu hiệu chia hết cho 9 bị ngắt giữa chừng, mất vế so sánh với chia hết cho 3."},
            "B": {"score": 2, "reason": "Đầy đủ 4 dấu hiệu chia hết 2, 5, 3, 9 trong ngữ cảnh hoàn chỉnh."},
            "C": {"score": 2, "reason": "Giống B."}
        }
    },
    {
        "position": 6,
        "page": 6,
        "title": "Số nguyên tố, ƯCLN, BCNN",
        "scores": {
            "A": {"score": 1, "reason": "Quy tắc tìm ƯCLN bị tách rời khỏi định nghĩa hai số nguyên tố cùng nhau."},
            "B": {"score": 2, "reason": "Đề mục số nguyên tố và mục ƯCLN/BCNN được phân đoạn chuẩn."},
            "C": {"score": 2, "reason": "Giống B."}
        }
    },
    {
        "position": 7,
        "page": 7,
        "title": "Số nguyên âm & Tập hợp Z",
        "scores": {
            "A": {"score": 2, "reason": "Khái niệm số 0 và số đối -a hiển thị đủ trong chunk đầu."},
            "B": {"score": 2, "reason": "Trọn vẹn mục ý nghĩa thực tế và cấu tạo tập hợp Z."},
            "C": {"score": 2, "reason": "Giống B."}
        }
    },
    {
        "position": 8,
        "page": 8,
        "title": "So sánh số nguyên",
        "scores": {
            "A": {"score": 1, "reason": "Quy tắc so sánh hai số nguyên âm bị ngắt khỏi ví dụ -9 < -4."},
            "B": {"score": 2, "reason": "Đầy đủ 4 quy tắc so sánh và ví dụ minh họa."},
            "C": {"score": 2, "reason": "Giống B."}
        }
    },
    {
        "position": 9,
        "page": 9,
        "title": "Phép cộng số nguyên",
        "scores": {
            "A": {"score": 1, "reason": "Cắt ngang giữa quy tắc cộng cùng dấu và ví dụ mang dấu âm."},
            "B": {"score": 2, "reason": "Chia thành 2 mục rõ ràng: cùng dấu và khác dấu kèm công thức."},
            "C": {"score": 2, "reason": "Giống B."}
        }
    },
    {
        "position": 10,
        "page": 10,
        "title": "Phép trừ & Quy tắc dấu ngoặc",
        "scores": {
            "A": {"score": 2, "reason": "Quy tắc đổi dấu khi bỏ ngoặc có dấu trừ hiển thị trọn vẹn."},
            "B": {"score": 2, "reason": "Phép trừ số nguyên và quy tắc dấu ngoặc được bảo toàn nguyên vẹn."},
            "C": {"score": 2, "reason": "Giống B."}
        }
    }
]

# 2. Grounding Quality trên 5 câu Test (q16 - q20)
GROUNDING_SAMPLES = [
    {
        "question_id": "q16",
        "question": "Hai đường chéo của hình thoi có những đặc điểm và tính chất hình học gì?",
        "gold_page": 26,
        "scores": {
            "A": {"score": 2, "reason": "Top-1 chứa đầy đủ đặc điểm vuông góc, cắt tại trung điểm và là trục đối xứng."},
            "B": {"score": 2, "reason": "Toàn bộ mục hình thoi có trong chunk top-1, grounding hoàn chỉnh."},
            "C": {"score": 2, "reason": "Filter 'hinh_hoc_truc_quan' loại sạch nhiễu, grounding tuyệt đối."}
        }
    },
    {
        "question_id": "q17",
        "question": "Công thức tính diện tích hình thang có đáy lớn a, đáy nhỏ b và chiều cao h là gì?",
        "gold_page": 29,
        "scores": {
            "A": {"score": 2, "reason": "Top-1 chứa đúng công thức S = ((a+b)*h)/2."},
            "B": {"score": 2, "reason": "Chunk mục hình thang chứa đầy đủ chu vi và diện tích."},
            "C": {"score": 2, "reason": "Top-1 chính xác tuyệt đối."}
        }
    },
    {
        "question_id": "q18",
        "question": "Hình tam giác đều và hình thang cân có tâm đối xứng không?",
        "gold_page": 30,
        "scores": {
            "A": {"score": 1, "reason": "Chunk top-1 chỉ chứa phần trục đối xứng, phải đọc chunk top-2 mới thấy khẳng định không có tâm đối xứng."},
            "B": {"score": 2, "reason": "Mục tâm đối xứng chứa trọn khẳng định tam giác đều và hình thang cân không có tâm đối xứng."},
            "C": {"score": 2, "reason": "Grounding đầy đủ ở rank 1."}
        }
    },
    {
        "question_id": "q19",
        "question": "Biểu đồ cột kép được sử dụng khi nào và cách phân biệt các cột giữa hai nhóm?",
        "gold_page": 34,
        "scores": {
            "A": {"score": 2, "reason": "Chunk top-1 chứa đủ định nghĩa và cách phân biệt màu sắc."},
            "B": {"score": 2, "reason": "Chunk mục biểu đồ cột kép nguyên vẹn, grounding xuất sắc."},
            "C": {"score": 2, "reason": "Chính xác tuyệt đối."}
        }
    },
    {
        "question_id": "q20",
        "question": "Công thức tính xác suất thực nghiệm của một sự kiện E khi thực hiện n lần thí nghiệm là gì?",
        "gold_page": 36,
        "scores": {
            "A": {"score": 2, "reason": "Công thức k/n và giải thích các đại lượng có trong chunk top-1."},
            "B": {"score": 2, "reason": "Grounding trọn vẹn định nghĩa và ví dụ gieo xúc xắc."},
            "C": {"score": 2, "reason": "Grounding hoàn chỉnh."}
        }
    }
]

audit_data = {
    "coherence_samples": COHERENCE_SAMPLES,
    "coherence_summary": {
        "A": {"avg_score": round(sum(s["scores"]["A"]["score"] for s in COHERENCE_SAMPLES) / len(COHERENCE_SAMPLES), 2), "n": len(COHERENCE_SAMPLES)},
        "B": {"avg_score": round(sum(s["scores"]["B"]["score"] for s in COHERENCE_SAMPLES) / len(COHERENCE_SAMPLES), 2), "n": len(COHERENCE_SAMPLES)},
        "C": {"avg_score": round(sum(s["scores"]["C"]["score"] for s in COHERENCE_SAMPLES) / len(COHERENCE_SAMPLES), 2), "n": len(COHERENCE_SAMPLES)}
    },
    "grounding_samples": GROUNDING_SAMPLES,
    "grounding_summary": {
        "A": {"counts": {"0": 0, "1": 1, "2": 4}, "avg_score": 1.8},
        "B": {"counts": {"0": 0, "1": 0, "2": 5}, "avg_score": 2.0},
        "C": {"counts": {"0": 0, "1": 0, "2": 5}, "avg_score": 2.0}
    }
}

audit_path = os.path.join(results_dir, "audit_labels.json")
with open(audit_path, "w", encoding="utf-8") as f:
    json.dump(audit_data, f, ensure_ascii=False, indent=2)

print(f"Đã lưu audit labels: {audit_path}")

