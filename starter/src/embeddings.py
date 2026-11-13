# -*- coding: utf-8 -*-
"""Choose a real embedding provider (API or local) and implement this contract."""
import os
import time
import traceback
from pathlib import Path
from typing import Protocol


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class GeminiEmbedder:
    """Real Gemini Embedder using gemini-embedding-001 (3072 dimensions).
    Tuân thủ quy định: Độ trễ 4 giây mỗi lần gọi API, tự động log lỗi vào file khi có sự cố.
    """

    def __init__(
        self,
        model_name: str = "models/gemini-embedding-001",
        api_key: str | None = None,
        log_file: Path | str | None = None,
        delay_seconds: float = 4.0
    ) -> None:
        self.model_name = model_name
        self.dimensions = 3072
        self.delay_seconds = delay_seconds
        
        # Thiết lập file log lỗi
        if log_file:
            self.log_file = Path(log_file)
        else:
            self.log_file = Path(__file__).resolve().parent.parent / "results" / "pipeline_errors.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Lấy API Key từ tham số hoặc biến môi trường hoặc file .env
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            env_file = Path(__file__).resolve().parent.parent / ".env"
            if env_file.exists():
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GEMINI_API_KEY="):
                            self.api_key = line.split("=", 1)[1].strip().strip('"\'')
                            break

        if not self.api_key:
            err_msg = "GEMINI_API_KEY chưa được cấu hình! Vui lòng điền API key vào file starter/.env."
            self._log_error("INIT", err_msg)
            raise ValueError(err_msg)

        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self.genai = genai

    def _log_error(self, context: str, error: Exception | str) -> None:
        """Ghi nhận chi tiết lỗi vào file log."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [ERROR] [{context}]: {str(error)}\n")
            if isinstance(error, Exception):
                f.write(traceback.format_exc() + "\n")
            f.write("-" * 50 + "\n")

    def embed_documents(self, texts: list[str], batch_size: int = 16) -> list[list[float]]:
        """Nhúng danh sách văn bản thành vector theo lô, độ trễ 4 giây giữa các lần gọi."""
        all_embeddings: list[list[float]] = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            max_retries = 3
            success = False

            for attempt in range(max_retries):
                try:
                    res = self.genai.embed_content(
                        model=self.model_name,
                        content=batch,
                        task_type="retrieval_document"
                    )
                    embeddings = res.get("embedding", [])
                    all_embeddings.extend(embeddings)
                    success = True
                    break
                except Exception as e:
                    self._log_error(f"embed_documents batch {i} (lần {attempt + 1})", e)
                    time.sleep(self.delay_seconds * 1.5)

            if not success:
                # Nếu batch thất bại sau retries, thử embed từng câu riêng lẻ
                print(f"[Cảnh báo] Lô {i} thất bại, chuyển sang embed từng phần tử...")
                for idx_sub, item in enumerate(batch):
                    sub_success = False
                    for sub_attempt in range(max_retries):
                        try:
                            res = self.genai.embed_content(
                                model=self.model_name,
                                content=item,
                                task_type="retrieval_document"
                            )
                            all_embeddings.append(res["embedding"])
                            sub_success = True
                            time.sleep(self.delay_seconds)
                            break
                        except Exception as e_sub:
                            self._log_error(f"embed_documents item {i + idx_sub} (lần {sub_attempt + 1})", e_sub)
                            time.sleep(self.delay_seconds * 1.5)
                    if not sub_success:
                        raise RuntimeError(f"Không thể embed văn bản mục {i + idx_sub} sau {max_retries} lần thử.")
            else:
                # Tuân thủ độ trễ 4 giây
                time.sleep(self.delay_seconds)

        return all_embeddings

    def embed_query(self, question: str) -> list[float]:
        """Nhúng câu hỏi truy vấn, tuân thủ độ trễ 4 giây."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                res = self.genai.embed_content(
                    model=self.model_name,
                    content=question,
                    task_type="retrieval_query"
                )
                time.sleep(self.delay_seconds)
                return res["embedding"]
            except Exception as e:
                self._log_error(f"embed_query (lần {attempt + 1}) - {question[:40]}", e)
                time.sleep(self.delay_seconds * 1.5)
        raise RuntimeError(f"Không thể embed câu hỏi: '{question}' sau {max_retries} lần thử.")
