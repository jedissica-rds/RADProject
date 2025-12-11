from typing import List, Dict, Tuple
from collections import Counter
from pathlib import Path
import pymupdf
import re

from pdf.cleaner import cleaning
from utils.stopwords import stopwords


class PDFExtractor:
    def __init__(self, file_path: Path):
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        self.file_path = file_path
        self.stopwords = stopwords
        self.document = pymupdf.open(self.file_path)

    # diminui uso de try catch!!!!!!
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _ensure_loaded(self) -> None:
        if not self.document:
            raise RuntimeError("Documento não carregado")

    def get_text(self) -> str:
        self._ensure_loaded()

        full_text = ""
        for page in self.document:
            text = page.get_text()
            text = cleaning(text)

            full_text += text

        return full_text

    def get_words(self, remove_stopwords: bool = False) -> List[str]:
        self._ensure_loaded()

        words: List[str] = []
        for page in self.document:
            text = page.get_text()
            text = text.replace("-\n", "").replace("\n", " ")
            words.extend(re.findall(r'\b[\wÀ-ÿ]+\b', text))

            # mais uma camada anti-artigo
            words = [w for w in words if len(w) > 1]

        if remove_stopwords:
            words = [w.lower() for w in words]
            words = [w for w in words if w not in self.stopwords]

        return words

    def get_page_count(self) -> int:
        self._ensure_loaded()
        return self.document.page_count

    def get_word_count(self) -> int:
        return len(self.get_words(remove_stopwords=False))

    def get_file_size(self) -> int:
        return self.file_path.stat().st_size

    def get_top_words(self, n: int = 10) -> List[Tuple[str, int]]:
        words = self.get_words(remove_stopwords=True)
        return Counter(words).most_common(n)

    def get_vocabulary_size(self) -> int:
        words = self.get_words(remove_stopwords=True)
        return len(set(words))

    def get_report(self) -> Dict:
        return {
            'page_count': self.get_page_count(),
            'word_count': self.get_word_count(),
            'file_size': self.get_file_size(),
            'vocabulary_size': self.get_vocabulary_size(),
            'top_words': self.get_top_words()
        }

    def close(self) -> None:
        if self.document:
            self.document.close()