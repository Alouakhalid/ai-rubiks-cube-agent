from typing import List, Dict, Any, Optional
from backend.app.config import settings


class CohereRAGClient:
    def __init__(self):
        self.api_key = settings.COHERE_API_KEY
        self.embed_model = settings.COHERE_EMBED_MODEL
        self.rerank_model = settings.COHERE_RERANK_MODEL
        self._client = None

        if self.api_key:
            try:
                import cohere
                self._client = cohere.Client(api_key=self.api_key)
            except Exception:
                self._client = None

    def is_available(self) -> bool:
        return self._client is not None

    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: int = 3,
    ) -> Optional[List[Dict[str, Any]]]:
        if not self._client or not documents:
            return None

        doc_texts = [
            f"{d['title']} - {d['category']}: {d['content']}" for d in documents
        ]

        try:
            response = self._client.rerank(
                model=self.rerank_model,
                query=query,
                documents=doc_texts,
                top_n=min(top_k, len(documents)),
            )

            reranked_results: List[Dict[str, Any]] = []
            for item in response.results:
                original_doc = documents[item.index]
                reranked_results.append({
                    "id": original_doc["id"],
                    "title": original_doc["title"],
                    "author": original_doc["author"],
                    "year": original_doc["year"],
                    "citation": original_doc["citation"],
                    "category": original_doc["category"],
                    "content": original_doc["content"],
                    "relevance_score": round(item.relevance_score, 4),
                    "rerank_engine": "cohere",
                })

            return reranked_results
        except Exception:
            return None


cohere_client = CohereRAGClient()
