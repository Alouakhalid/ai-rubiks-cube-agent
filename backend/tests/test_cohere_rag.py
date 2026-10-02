import pytest
from backend.app.rag.cohere_client import cohere_client
from backend.app.rag.knowledge_base import knowledge_base
from backend.app.config import settings


def test_cohere_client_configuration():
    assert settings.COHERE_API_KEY != ""
    assert settings.COHERE_RERANK_MODEL == "rerank-v3.5"
    assert cohere_client.is_available()


def test_knowledge_base_hybrid_query():
    results = knowledge_base.query("Kociemba two-phase coset subgroup", top_k=2)
    assert len(results) > 0
    assert "id" in results[0]
    assert "relevance_score" in results[0]
    assert "citation" in results[0]


def test_qwen_groq_configuration():
    assert settings.GROQ_API_KEY != ""
    assert "qwen" in settings.GROQ_MODEL.lower()
