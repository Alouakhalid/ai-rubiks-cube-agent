import re
import math
from typing import List, Dict, Any, Tuple
from collections import Counter


class KnowledgeRetriever:
    def __init__(self, documents: List[Dict[str, Any]]):
        self.documents = documents
        self.k1 = 1.5
        self.b = 0.75
        self.doc_tokens: List[List[str]] = []
        self.doc_lens: List[int] = []
        self.avg_dl: float = 0.0
        self.df: Counter = Counter()
        self.n_docs = len(documents)

        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
        return [w for w in cleaned.split() if len(w) > 1]

    def _build_index(self) -> None:
        total_len = 0
        for doc in self.documents:
            corpus_text = f"{doc['title']} {doc['category']} {doc['content']}"
            tokens = self._tokenize(corpus_text)
            self.doc_tokens.append(tokens)
            l = len(tokens)
            self.doc_lens.append(l)
            total_len += l

            unique_terms = set(tokens)
            for t in unique_terms:
                self.df[t] += 1

        self.avg_dl = (total_len / self.n_docs) if self.n_docs > 0 else 1.0

    def _score_bm25(self, query_tokens: List[str], doc_idx: int) -> float:
        score = 0.0
        doc_len = self.doc_lens[doc_idx]
        tokens = self.doc_tokens[doc_idx]
        tf = Counter(tokens)

        for q in query_tokens:
            if q not in self.df:
                continue

            n = self.df[q]
            idf = math.log(1.0 + (self.n_docs - n + 0.5) / (n + 0.5))
            f = tf.get(q, 0)

            numerator = f * (self.k1 + 1.0)
            denominator = f + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_dl))
            score += idf * (numerator / denominator)

        return score

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        scores: List[Tuple[int, float]] = []
        for i in range(self.n_docs):
            s = self._score_bm25(query_tokens, i)
            if s > 0.0:
                scores.append((i, s))

        scores.sort(key=lambda x: x[1], reverse=True)
        results: List[Dict[str, Any]] = []

        for idx, score in scores[:top_k]:
            doc = self.documents[idx]
            results.append({
                "id": doc["id"],
                "title": doc["title"],
                "author": doc["author"],
                "year": doc["year"],
                "citation": doc["citation"],
                "category": doc["category"],
                "content": doc["content"],
                "relevance_score": round(score, 4),
            })

        return results
