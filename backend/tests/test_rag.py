import pytest
from backend.app.rag.knowledge_base import knowledge_base


def test_rag_retrieves_kociemba():
    results = knowledge_base.query("Kociemba two-phase coset subgroup")
    assert len(results) > 0
    assert "Kociemba" in results[0]["title"] or "Kociemba" in results[0]["author"]
    assert results[0]["relevance_score"] > 0


def test_rag_retrieves_singmaster():
    results = knowledge_base.query("Singmaster parity laws edge corner orientation")
    assert len(results) > 0
    top = results[0]
    assert "Singmaster" in top["author"] or "Parity" in top["content"]


def test_rag_retrieves_gods_number():
    results = knowledge_base.query("God number 20 superflip Rokicki")
    assert len(results) > 0
    assert any("20" in r["title"] or "20" in r["content"] for r in results)


def test_format_context_for_prompt():
    context = knowledge_base.format_context_for_prompt("CFOP Fridrich cross F2L")
    assert "SOURCE:" in context
    assert "CITATION:" in context
    assert "EXCERPT:" in context
