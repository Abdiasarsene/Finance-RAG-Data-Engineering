# chunker/core/utils.py
import uuid
from typing import List, Dict
from logs.logger import logger


class ChunkUtils:
    def __init__(self):
        pass

    def build_chunks(self, segments: List[str]) -> List[Dict]:
        try:
            chunks = []
            offset = 0
            for i, segment in enumerate(segments):
                chunks.append({
                    "chunk_id": str(uuid.uuid4()),
                    "order": i,
                    "content": segment.strip(),
                    "start": offset,
                    "end": offset + len(segment),
                })
                offset += len(segment)
            return chunks
        except Exception as e:
            logger.error("Erreur lors de la construction des chunks", error=str(e))
            raise