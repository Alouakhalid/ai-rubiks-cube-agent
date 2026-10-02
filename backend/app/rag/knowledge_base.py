from typing import List, Dict, Any, Optional
from backend.app.rag.sources import KNOWLEDGE_DOCUMENTS
from backend.app.rag.retriever import KnowledgeRetriever
from backend.app.rag.cohere_client import cohere_client


class KnowledgeBase:
    def __init__(self, documents: Optional[List[Dict[str, Any]]] = None):
        self.documents = documents if documents is not None else KNOWLEDGE_DOCUMENTS
        self.retriever = KnowledgeRetriever(self.documents)
        self.cohere = cohere_client

    def query(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        cohere_results = self.cohere.rerank(
            query=query_text,
            documents=self.documents,
            top_k=top_k,
        )
        if cohere_results is not None and len(cohere_results) > 0:
            return cohere_results

        bm25_results = self.retriever.retrieve(query_text, top_k=top_k)
        for r in bm25_results:
            r["rerank_engine"] = "bm25_fallback"
        return bm25_results

    def format_context_for_prompt(self, query_text: str, top_k: int = 2) -> str:
        results = self.query(query_text, top_k=top_k)
        if not results:
            return ""

        formatted_parts: List[str] = []
        for r in results:
            engine_tag = r.get("rerank_engine", "cohere")
            part = (
                f"SOURCE: {r['title']} ({r['year']}) [Retrieved via {engine_tag}]\n"
                f"CITATION: {r['citation']}\n"
                f"EXCERPT: {r['content']}"
            )
            formatted_parts.append(part)

        return "\n\n".join(formatted_parts)

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        for d in self.documents:
            if d["id"] == doc_id:
                return d
        return None


knowledge_base = KnowledgeBase()
