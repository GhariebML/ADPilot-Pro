"""Advanced semantic and hierarchical document chunker."""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional
from uuid import uuid4
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class SemanticChunker:
    """Splits documents into semantically coherent chunks with heading hierarchy and provenance metadata."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 75,
        separators: Optional[List[str]] = None,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n## ", "\n### ", "\n#### ", "\n\n", "\n", ". ", " "]

    def chunk_document(
        self,
        text: str,
        document_name: str,
        base_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """Chunks a raw text document, attaching hierarchical section headers and unique chunk IDs."""
        if not text or not text.strip():
            return []

        base_meta = base_metadata or {}
        chunks: List[Document] = []
        
        # 1. Parse markdown headers to track sections
        sections = self._split_by_headers(text)

        chunk_idx = 0
        for header, section_text in sections:
            # 2. Sub-chunk long sections using sliding window
            sub_chunks = self._recursive_split(section_text, self.chunk_size, self.chunk_overlap)
            for sub_text in sub_chunks:
                clean_text = sub_text.strip()
                if not clean_text:
                    continue

                chunk_id = f"chk-{uuid4().hex[:8]}"
                chunk_meta = {
                    **base_meta,
                    "document_name": document_name,
                    "chunk_id": chunk_id,
                    "chunk_index": chunk_idx,
                    "section_header": header or "General",
                    "character_count": len(clean_text),
                }
                chunks.append(Document(page_content=clean_text, metadata=chunk_meta))
                chunk_idx += 1

        logger.info(
            "SemanticChunker | Document '%s' split into %d chunks (avg %d chars)",
            document_name,
            len(chunks),
            sum(len(c.page_content) for c in chunks) // max(1, len(chunks)),
        )
        return chunks

    def _split_by_headers(self, text: str) -> List[tuple[str, str]]:
        """Splits markdown text into (header, content) tuples."""
        header_pattern = re.compile(r"^(#{1,4}\s+.+)$", re.MULTILINE)
        splits = header_pattern.split(text)

        sections: List[tuple[str, str]] = []
        current_header = "Overview"

        if splits and not header_pattern.match(splits[0]):
            sections.append((current_header, splits[0]))
            splits = splits[1:]

        for i in range(0, len(splits), 2):
            if i + 1 < len(splits):
                header = splits[i].strip("#").strip()
                content = splits[i + 1]
                sections.append((header, content))
            elif i < len(splits):
                sections.append((current_header, splits[i]))

        return sections if sections else [("General", text)]

    def _recursive_split(self, text: str, max_size: int, overlap: int) -> List[str]:
        """Recursively splits text into chunks of at most max_size with overlap."""
        if len(text) <= max_size:
            return [text]

        for sep in self.separators:
            if sep in text:
                parts = text.split(sep)
                result = []
                current_chunk = ""
                for p in parts:
                    candidate = f"{current_chunk}{sep}{p}" if current_chunk else p
                    if len(candidate) <= max_size:
                        current_chunk = candidate
                    else:
                        if current_chunk:
                            result.append(current_chunk)
                        current_chunk = p
                if current_chunk:
                    result.append(current_chunk)
                if len(result) > 1:
                    return result

        # Hard fallback chunking
        result = []
        start = 0
        while start < len(text):
            end = min(start + max_size, len(text))
            result.append(text[start:end])
            start += max_size - overlap
        return result
