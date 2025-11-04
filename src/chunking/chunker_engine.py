# src/chunking/chunker_engine.py
import time
from typing import List, Dict
from logs.logger import logger
from metrics.monitoring import (
    increment_messages,
    observe_processing_time,
    increment_errors
)
from src.chunking.chunker_strategies import ChunkStrategies
from src.chunking.chunk_utils import ChunkerUtils

# ====== CHUNKING ENGINE ======
class ChunkerEngine:
    # Set up
    def __init__(self, config: dict):
        self.strategy = config.get("strategy", "by_tokens")
        self.max_tokens = config.get("max_tokens", 512)
        self.overlap = config.get("overlap", 50)
        self.worker_name = "ChunkerWorker"
        self.strategies = ChunkStrategies(self.max_tokens, self.overlap)
        self.utils = ChunkerUtils()

    # Apply chunking
    def chunk(self, text: str) -> List[Dict]:
        start_time = time.time()

        try:
            if not text or not text.strip():
                logger.warning("Texte vide reçu pour chunking.")
                return []
            if self.strategy == "by_sentence":
                chunks = self.strategies.by_sentence(text)
            elif self.strategy == "by_paragraph":
                chunks = self.strategies.by_paragraph(text)
            else:
                chunks = self.strategies.by_tokens(text)

            # Metrics Prometheus
            processing_time = time.time() - start_time
            observe_processing_time(self.worker_name, processing_time)
            increment_messages(self.worker_name, status="success")

            logger.info(
                "Chunking terminé",
                strategy=self.strategy,
                chunks_count=len(chunks),
                processing_time=f"{processing_time:.3f}s",
            )
            return self.utils.build_chunks(chunks)
        except Exception as e:
            increment_errors(self.worker_name, error_type=type(e).__name__)
            logger.error("Erreur lors du chunking", error=str(e))
            raise e