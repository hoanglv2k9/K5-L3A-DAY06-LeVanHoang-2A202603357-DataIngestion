# -*- coding: utf-8 -*-
"""Vector store implementation using Qdrant (Persistent embedded vector store)."""
import os
import uuid
from typing import Any
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

from .models import Chunk


class VectorStore:
    """Persistent Qdrant Vector Store supporting Cosine metric and Metadata Filtering."""

    def __init__(self, storage_path: str = "results/qdrant_db", dimensions: int = 3072) -> None:
        self.storage_path = storage_path
        self.dimensions = dimensions
        os.makedirs(self.storage_path, exist_ok=True)
        self.client = QdrantClient(path=self.storage_path)

    def create_schema(self, collection_name: str) -> None:
        """Create or recreate collection with cosine metric and dimension check."""
        collections = [c.name for c in self.client.get_collections().collections]
        if collection_name not in collections:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=self.dimensions, distance=Distance.COSINE)
            )

    def upsert(self, collection_name: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Upsert chunks and vectors with deterministic UUIDs to prevent duplication."""
        self.create_schema(collection_name)
        
        points: list[PointStruct] = []
        for chunk, vector in zip(chunks, vectors):
            # Sinh UUID cố định dựa trên chunk_id (idempotent - nạp lại không trùng)
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.chunk_id))
            payload = {
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "source": chunk.source,
                "page": chunk.page,
                "text": chunk.text,
                **chunk.metadata
            }
            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            )

        # Upsert theo batch để đảm bảo ổn định
        batch_size = 50
        for i in range(0, len(points), batch_size):
            self.client.upsert(
                collection_name=collection_name,
                points=points[i:i + batch_size]
            )

    def search(
        self,
        collection_name: str,
        query_vector: list[float],
        top_k: int = 3,
        filters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Search top-k chunks by Cosine similarity, applying metadata filters if provided."""
        q_filter = None
        if filters:
            conditions = []
            for k, v in filters.items():
                if v is not None:
                    conditions.append(
                        FieldCondition(key=k, match=MatchValue(value=v))
                    )
            if conditions:
                q_filter = Filter(must=conditions)

        res = self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=top_k,
            query_filter=q_filter
        )

        results = []
        for pt in res.points:
            results.append({
                "chunk_id": pt.payload.get("chunk_id", str(pt.id)),
                "text": pt.payload.get("text", ""),
                "score": float(pt.score) if pt.score is not None else 0.0,
                "document_id": pt.payload.get("document_id", ""),
                "source": pt.payload.get("source", ""),
                "page": pt.payload.get("page", 0),
                "metadata": {
                    k: v for k, v in pt.payload.items()
                    if k not in ["text", "chunk_id", "document_id", "source", "page"]
                }
            })
        return results
