"""BM25 sparse lexical retrieval engine."""

from __future__ import annotations

import logging
import math
import re
from typing import Dict, List, Optional, Tuple
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class BM25Index:
    """Okapi BM25 sparse keyword inverted index for high-precision lexical retrieval."""

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.documents: List[Document] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_length: float = 0.0
        self.doc_count: int = 0
        self.inverted_index: Dict[str, Dict[int, int]] = {}  # term -> {doc_idx: freq}
        self.doc_freqs: Dict[str, int] = {}  # term -> doc_count

    def tokenize(self, text: str) -> List[str]:
        """Lowercases, removes punctuation, and tokenizes text into word tokens."""
        clean = re.sub(r"[^\w\s]", " ", text.lower())
        return [tok for tok in clean.split() if len(tok) > 1]

    def index_documents(self, documents: List[Document]) -> None:
        """Indexes a collection of documents into the BM25 inverted index."""
        self.documents = documents
        self.doc_count = len(documents)
        self.doc_lengths = []
        self.inverted_index = {}
        self.doc_freqs = {}

        if not documents:
            self.avg_doc_length = 0.0
            return

        total_length = 0
        for doc_idx, doc in enumerate(documents):
            tokens = self.tokenize(doc.page_content)
            doc_len = len(tokens)
            self.doc_lengths.append(doc_len)
            total_length += doc_len

            term_counts: Dict[str, int] = {}
            for t in tokens:
                term_counts[t] = term_counts.get(t, 0) + 1

            for term, count in term_counts.items():
                if term not in self.inverted_index:
                    self.inverted_index[term] = {}
                self.inverted_index[term][doc_idx] = count
                self.doc_freqs[term] = self.doc_freqs.get(term, 0) + 1

        self.avg_doc_length = total_length / max(1, self.doc_count)
        logger.info(
            "BM25Index | Indexed %d documents (%d unique terms, avg doc length: %.1f tokens)",
            self.doc_count,
            len(self.inverted_index),
            self.avg_doc_length,
        )

    def search(
        self,
        query: str,
        k: int = 5,
        filter_fn: Optional[callable] = None,
    ) -> List[Tuple[Document, float]]:
        """Performs Okapi BM25 scoring against the indexed corpus."""
        if not self.documents or not query.strip():
            return []

        query_tokens = self.tokenize(query)
        if not query_tokens:
            return []

        scores: Dict[int, float] = {i: 0.0 for i in range(self.doc_count)}

        for token in query_tokens:
            if token not in self.inverted_index:
                continue

            # Inverse Document Frequency (IDF) calculation
            df = self.doc_freqs.get(token, 0)
            idf = math.log(((self.doc_count - df + 0.5) / (df + 0.5)) + 1.0)

            for doc_idx, tf in self.inverted_index[token].items():
                doc_len = self.doc_lengths[doc_idx]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / max(1.0, self.avg_doc_length)))
                scores[doc_idx] += idf * (numerator / max(0.001, denominator))

        # Filter and rank candidates
        results = []
        for doc_idx, score in scores.items():
            if score > 0.0:
                doc = self.documents[doc_idx]
                if filter_fn is None or filter_fn(doc):
                    results.append((doc, float(score)))

        results.sort(key=lambda item: item[1], reverse=True)
        return results[:k]
