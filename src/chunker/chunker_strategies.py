# chunker/chunk_strategies.py
import re
from typing import List
from logs.logger import logger


class ChunkStrategies:
    """
    Définit les stratégies de découpage.
    """

    def __init__(self, max_tokens: int = 512, overlap: int = 50):
        self.max_tokens = max_tokens
        self.overlap = overlap

    def by_sentence(self, text: str) -> List[str]:
        try:
            sentences = re.split(r'(?<=[.!?]) +', text)
            return [s.strip() for s in sentences if s.strip()]
        except Exception as e:
            logger.error("Erreur dans la stratégie by_sentence", error=str(e))
            raise

    def by_paragraph(self, text: str) -> List[str]:
        try:
            paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
            return paragraphs
        except Exception as e:
            logger.error("Erreur dans la stratégie by_paragraph", error=str(e))
            raise

    def by_tokens(self, text: str) -> List[str]:
        try:
            tokens = text.split()
            chunks, current, count = [], [], 0

            for token in tokens:
                current.append(token)
                count += 1
                if count >= self.max_tokens:
                    chunks.append(" ".join(current))
                    if self.overlap > 0:
                        current = current[-self.overlap:]
                        count = len(current)
                    else:
                        current, count = [], 0

            if current:
                chunks.append(" ".join(current))
            return chunks

        except Exception as e:
            logger.error("Erreur dans la stratégie by_tokens", error=str(e))
            raise