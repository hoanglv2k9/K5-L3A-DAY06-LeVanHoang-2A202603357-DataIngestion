# Báo cáo cá nhân — Day 6: Data Ingestion Engineering

- **Họ và tên:** Lê Văn Hoàng
- **MSSV:** 2A202603357
- **Lớp:** L3A
- **Chủ đề & Corpus:** Sổ tay Kiến thức và Trọng tâm Lý thuyết Toán lớp 6 (Chương trình Giáo dục Phổ thông 2018)
- **Repo bài nộp:** `K5-L3A-DAY06-LeVanHoang-2A202603357-DataIngestion`

---

## Dữ liệu và pipeline

- **Chủ đề, nguồn/quyền, số trang và quy tắc tính trang:**
  - **Chủ đề:** Toàn bộ kiến thức trọng tâm môn Toán lớp 6 (Tập 1 và Tập 2) theo Chương trình GDPT 2018, bao gồm 6 chương: Số tự nhiên, Số nguyên, Phân số, Số thập phân, Hình học trực quan và Một số yếu tố thống kê & xác suất.
  - **Nguồn & Quyền:** Tài nguyên Giáo dục Mở (OER), phát hành theo giấy phép **Creative Commons CC BY-NC-SA 4.0** (Attribution-NonCommercial-ShareAlike), ghi nhận tại [data/manifest.json](../../starter/data/manifest.json).
  - **Số trang & Quy tắc tính:** Tài liệu có tổng cộng **36 trang vật lý**, tương ứng **36 trang nội dung hữu ích** (từ trang 1 đến trang 36). Không có trang bìa, trang trắng, mục lục hay trang tài liệu tham khảo dư thừa. Tổng dung lượng văn bản là **27.459 ký tự**, trung bình ~760 ký tự/trang chữ tiếng Việt học thuật chuẩn hóa.

- **Chuẩn hóa, lỗi và giới hạn:**
  - Văn bản được xử lý qua hàm `normalize_text` trong [ingestion.py](../../starter/src/ingestion.py): Chuẩn hóa Unicode toàn diện theo dạng dựng sẵn **NFC** (`unicodedata.normalize`), loại bỏ khoảng trắng và tab thừa nhưng giữ lại cấu trúc phân cấp tiêu đề Markdown (`### 1.`, `### 2.`) và dấu gạch đầu dòng danh sách.
  - Các ký hiệu toán học đặc thù ($\mathbb{N}, \mathbb{N}^*, \mathbb{Z}, \in, \notin, \vdots$) được kiểm tra tương thích khi xuất PDF và trích xuất qua `pypdf`. Giới hạn: Chưa xử lý các công thức LaTeX toán học phức tạp dạng nhiều tầng phân số mà được chuyển tự thành dạng biểu thức chuẩn ($a/b$).

- **Embedding model/provider/version/số chiều, vector store/version, metric, lệnh chạy và chi phí:**
  - **Embedding Provider & Model:** Google Gemini API (`models/gemini-embedding-001`), số chiều vector: **3072 dimensions**, task type phân biệt `retrieval_document` và `retrieval_query`.
  - **Vector Store:** **Qdrant Embedded** (`qdrant-client` v1.20.0), lưu trữ bền vững (persistent on-disk) tại thư mục `starter/results/qdrant_db`, hỗ trợ tìm kiếm vector chính xác và metadata payload filtering.
  - **Similarity Metric:** **Cosine Similarity** (`Distance.COSINE`).
  - **Lệnh chạy:** `cd starter && python -m src.run`
  - **Chi phí & Thời gian:** Chi phí **$0.00** (Google AI Studio Free Tier). Thời gian chạy Strategy A là 33.81s (85 chunks); Strategy B là 114.70s (67 chunks, tuân thủ độ trễ 4 giây/lần gọi để chống rate limit).

- **Metadata bắt buộc, trường lọc bổ sung, nguồn giá trị và lý do chọn:**
  - **Metadata bắt buộc:** `document_id` (`toan-6-gdpt2018`), `source` (`toan_6_tap_1_va_2_gdpt2018.pdf`), `page` (số trang vật lý 1–36).
  - **Trường lọc bổ sung (`section`):** Nhận 1 trong 6 giá trị tương ứng 6 chương SGK:
    - `so_tu_nhien` (Trang 1 - 6)
    - `so_nguyen` (Trang 7 - 12)
    - `phan_so` (Trang 13 - 18)
    - `so_thap_phan` (Trang 19 - 24)
    - `hinh_hoc_truc_quan` (Trang 25 - 30)
    - `thong_ke_xac_suat` (Trang 31 - 36)
  - **Lý do chọn:** Phân loại rõ ràng ranh giới kiến thức giữa các phân môn, cho phép kiểm chứng chính xác khả năng lọc phạm vi (Metadata Filtering) khi câu hỏi chỉ định rõ ngữ cảnh (ví dụ chỉ tìm kiếm trong phần hình học trực quan).

---

## Cấu hình và benchmark

- **A / B / C (tham số cụ thể, khác biệt duy nhất B–C):**
  - **Strategy A (Fixed-size Window):** Chunking kích thước cố định `chunk_size = 500` ký tự, `overlap = 50` ký tự. Gắn metadata `document_id`, `source`, `page`, `section`. **Không áp dụng bộ lọc** (No Filter). Sinh ra **85 chunks**.
  - **Strategy B (Structure-aware Paragraph):** Chunking theo cấu trúc đoạn văn bản và tiêu đề `###`, nhóm các đoạn nhỏ có giới hạn `max_size = 800` ký tự, `overlap = 0`. Cùng metadata, **không áp dụng bộ lọc**. Sinh ra **67 chunks**.
  - **Strategy C (Metadata Filtered):** Cấu hình chunking **giống hệt Strategy B** (cùng 67 chunks, dùng chung vector collection trong Qdrant). Khác biệt duy nhất: **Áp dụng lọc metadata theo trường `section`** khi câu hỏi có điều kiện filter. (Khác biệt A–B là kỹ thuật phân mảnh văn bản; khác biệt B–C là việc bật/tắt metadata filter để cô lập tác động của metadata).

- **≥20 câu: phân chia ≥15 dev / ≥5 test, câu metadata filter và cách kiểm chứng evidence:**
  - Bộ câu hỏi gồm đúng **20 câu** được lưu tại [benchmark/benchmark_questions.json](../../benchmark/benchmark_questions.json).
  - Tách trước độc lập: **15 câu Dev Split** (`q01` đến `q15`) và **5 câu Test Split** (`q16` đến `q20`).
  - Gồm đầy đủ các loại câu hỏi: Trực tiếp (`q01`, `q02`), Công thức (`q03`, `q14`, `q17`, `q20`), Thứ tự tính (`q04`), Điều kiện/Dấu hiệu (`q05`), Ngoại lệ (`q09`, `q18`), So sánh (`q19`), và **3 câu kiểm tra Metadata Filter** (`q07` [Dev], `q10` [Dev], `q16` [Test]).
  - **Cách kiểm chứng evidence:** Mỗi câu hỏi đều đối chiếu văn bản gốc trong file PDF, lưu trọn vẹn `gold_page` và `evidence_quote` trích nguyên văn từng câu chữ.

- **Tiêu chí chọn chiến lược đã chốt trước khi xem test:**
  - **Tiêu chí 1 (Bắt buộc):** Evidence Hit@3 trên tập Dev phải đạt tối thiểu 95%.
  - **Tiêu chí 2 (Chất lượng):** Tính mạch lạc (Chunk Coherence) phải đạt điểm trung bình $\ge 1.8 / 2.0$ để tránh làm đứt gãy công thức và quy tắc toán học.
  - **Tiêu chí 3 (Hiệu quả tài nguyên):** Số lượng chunk và dung lượng lưu trữ ít hơn để tiết kiệm chi phí embedding và tăng tốc độ tìm kiếm.

---

## Kết quả

### Bảng 1: Hiệu năng Truy xuất và Tài nguyên (Retrieval Accuracy & Resources)

| Strategy | Split | Hit@1 (n/N) | Evidence Hit@3 (n/N) | Chunk count | Thời gian ingest | Chi phí |
|---|---|---|---|---|---|---|
| **Strategy A** (Fixed 500) | Dev | **15/15 (100.0%)** | **15/15 (100.0%)** | 85 chunks | 33.81s | $0.00 |
| **Strategy A** (Fixed 500) | Test | **5/5 (100.0%)** | **5/5 (100.0%)** | 85 chunks | - | $0.00 |
| **Strategy B** (Paragraph 800) | Dev | **14/15 (93.3%)** | **15/15 (100.0%)** | 67 chunks | 114.70s | $0.00 |
| **Strategy B** (Paragraph 800) | Test | **5/5 (100.0%)** | **5/5 (100.0%)** | 67 chunks | - | $0.00 |
| **Strategy C** (B + Filter) | Dev | **14/15 (93.3%)** | **15/15 (100.0%)** | 67 chunks | Dùng chung B | $0.00 |
| **Strategy C** (B + Filter) | Test | **5/5 (100.0%)** | **5/5 (100.0%)** | 67 chunks | - | $0.00 |

### Bảng 2: Đánh giá Thủ công 5 Khía cạnh (Audit & Quality Metrics)

| Strategy | Coherence trung bình /2 (n) | Metadata đủ và đúng (n/N) | Filter tuân thủ (n/N hoặc N/A) | Grounding 0/1/2 (số câu) và trung bình /2 |
|---|---|---|---|---|
| **Strategy A** | **1.30 / 2.0** (n=10) | **15/15 (100%)** | N/A (không áp dụng filter) | Mức 0: 0, Mức 1: 1, Mức 2: 4 (TB: **1.80 / 2.0**) |
| **Strategy B** | **1.90 / 2.0** (n=10) | **15/15 (100%)** | N/A (không áp dụng filter) | Mức 0: 0, Mức 1: 0, Mức 2: 5 (TB: **2.00 / 2.0**) |
| **Strategy C** | **1.90 / 2.0** (n=10) | **15/15 (100%)** | **1/1 câu (100%)** (3/3 chunks top-3) | Mức 0: 0, Mức 1: 0, Mức 2: 5 (TB: **2.00 / 2.0**) |

- **Đường dẫn artifacts:**
  - File Trace chi tiết: [starter/results/traces.json](../../starter/results/traces.json)
  - File Tóm tắt kết quả: [starter/results/summary.json](../../starter/results/summary.json)
  - File Nhật ký thí nghiệm: [artifacts/experiment_log.csv](../../artifacts/experiment_log.csv)
  - File Nhãn chấm thủ công: [starter/results/audit_labels.json](../../starter/results/audit_labels.json)
  - File Log lỗi hệ thống: [starter/results/pipeline_errors.log](../../starter/results/pipeline_errors.log)
- **Cách chọn mẫu audit:**
  - *Chunk Coherence:* Cố định trước 10 vị trí nội dung nguồn tại 10 trang đầu tiên (Trang 1 đến Trang 10) trên cả 3 chiến lược để chấm thang điểm 0–2.
  - *Metadata Usefulness & Grounding:* Chấm toàn bộ 5 câu thuộc tập Test (`q16` đến `q20`) nhân với Top-3 kết quả truy xuất (15 bản ghi).

---

## Phân tích và kết luận

- **So sánh A–B và B–C; 2 ví dụ sai có ID câu và nguồn:**
  - **So sánh A–B (Tác động của Chunking):** Strategy A tạo ra 85 chunk, nhiều hơn 26.8% so với Strategy B (67 chunk) do cơ chế fixed-size kèm overlap 50 ký tự. Về retrieval thô, Strategy A đạt Hit@1 = 15/15 trên dev, nhỉnh hơn Strategy B (14/15). Tuy nhiên, về mặt ngữ nghĩa và độ mạch lạc, Strategy A kém hơn rõ rệt (Coherence 1.30 vs 1.90). Các cửa sổ 500 ký tự cắt ngang qua giữa các mệnh đề điều kiện hoặc công thức toán, khiến người đọc hoặc LLM bị thiếu thông tin mở đầu.
  - **So sánh B–C (Tác động của Metadata Filter):** Do bộ benchmark có độ đặc thù cao và model embedding `gemini-embedding-001` (3072 chiều) phân biệt ngữ nghĩa rất xuất sắc nên Hit@3 của cả B và C đều đạt 100%. Tuy nhiên, Strategy C mang lại giá trị kiểm soát tuyệt đối: Đối với câu `q16` (hỏi về đặc điểm hình thoi), Strategy C loại bỏ 100% các đoạn vector thuộc các chương khác, đảm bảo cả 3/3 kết quả trong top-3 đều thuộc đúng phân vùng `hinh_hoc_truc_quan`.
  - **Ví dụ sai 1 — Câu `q11` (Strategy B & C, Dev Split, Gold Page 14):**
    - *Câu hỏi:* "Để rút gọn một phân số về phân số tối giản chỉ trong một lần ta làm thế nào?"
    - *Lỗi ghi nhận:* Hit@1 = False (đạt Hit@3 ở vị trí Rank 2).
    - *Nguyên nhân:* Tại trang 14, Strategy B chia thành 2 chunk theo tiêu đề con. Chunk ở vị trí Rank 1 bắt đầu bằng: *"một lần, ta chia cả tử và mẫu của phân số đó cho ước chung lớn nhất (ƯCLN) của chúng"*, bị khuyết mất mệnh đề chính ở đầu câu: *"Muốn rút gọn một phân số về phân số tối giản chỉ trong"*. Do đó, chunk ở Rank 1 không thỏa mãn tiêu chí so khớp đầy đủ bằng chứng, phải tới Rank 2 mới chứa đoạn văn bản hoàn chỉnh.
  - **Ví dụ sai 2 — Câu `q08` (Strategy A, Dev Split, Gold Page 10):**
    - *Câu hỏi:* "Quy tắc bỏ dấu ngoặc khi đằng trước có dấu trừ được thực hiện ra sao?"
    - *Lỗi ghi nhận:* Chunk Coherence chỉ đạt mức 1/2.
    - *Nguyên nhân:* Cửa sổ cố định 500 ký tự ngắt đúng vào giữa câu quy tắc bỏ ngoặc, làm đứt đoạn điều kiện đổi dấu `+` thành `-` sang chunk tiếp theo. Người đọc nếu chỉ nhìn vào chunk đầu tiên sẽ không hiểu đầy đủ quy tắc đổi dấu của tất cả các số hạng.

- **Chiến lược chọn, đánh đổi, điều kiện áp dụng:**
  - **Chiến lược được chọn:** **Strategy C** (hoặc Strategy B khi người dùng không cung cấp metadata lọc).
  - **Đánh đổi (Trade-offs):** Strategy C/B đánh đổi việc Hit@1 có thể giảm nhẹ trong trường hợp ranh giới đoạn văn bị chia nhỏ (như câu `q11`), để đổi lấy: (1) Tính mạch lạc vượt trội (Coherence 1.90/2.0), (2) Chất lượng thông tin nền hoàn hảo (Grounding 2.0/2.0 trên toàn bộ tập test), và (3) Giảm 21.2% số lượng chunk cần lưu trữ (67 so với 85), giúp tiết kiệm tài nguyên database và chi phí API.
  - **Điều kiện áp dụng:** Rất phù hợp cho các tài liệu có cấu trúc phân mục rõ ràng như sách giáo trình, cẩm nang kỹ thuật, luật hoặc sổ tay quy chế nội bộ.

- **Hạn chế của dữ liệu, nhãn, test nhỏ, đo thời gian/chi phí:**
  - Dữ liệu tập trung vào chương trình Toán lớp 6 đơn ngữ (tiếng Việt), chưa bao gồm các cấu trúc bảng biểu phức tạp hoặc sơ đồ hình học dạng ảnh raster.
  - Tập Test gồm 5 câu là kích thước mẫu phù hợp trong khuôn khổ lab 4 giờ để audit thủ công, nhưng chưa đủ lớn để ngoại suy kết luận thống kê tổng quát cho toàn bộ hệ thống lớn.
  - Người chấm nhãn thủ công là tác giả (sinh viên thực hiện), có thể tiềm ẩn sai lệch chủ quan (subjective bias).

- **Nếu làm lại hoặc mở rộng, cải tiến gì?:**
  - **Sentence-Window Retrieval / Parent-Document Retrieval:** Chia chunk nhỏ theo từng câu để embedding đạt độ tập trung cao nhất, nhưng khi truy xuất sẽ trả về toàn bộ đoạn văn bản cha (`parent chunk`) chứa câu đó để đảm bảo Hit@1 luôn đạt 100% mà không bị đứt câu như trường hợp `q11`.
  - **Hybrid Search (Dense + BM25):** Kết hợp vector embedding của Gemini với bộ chỉ mục từ khóa BM25 để tối ưu hóa việc tìm kiếm các công thức toán học và ký hiệu số học chính xác.

