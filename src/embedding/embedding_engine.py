# src/embedding/embedding_engine.py
from logs.logger import logger
import time

# ====== EMBEDDING ENGINE ======
class EmbeddingEngine:
    # Set up
    def __init__(self, config: dict, model_client=None):
        self.model_name = config.get("model", "text-embedding-3-small")
        self.dimension = config.get("dimension", 1536)
        self.batch_size = config.get("batch_size", 32)
        self.model_client = model_client

    # Apply embedding
    def embed(self, text: str):
        if not text.strip():
            return [0.0] * self.dimension  # vector empty
        try:
            # Call API
            vector = self.model_client.get_embedding(text, model=self.model_name)
            return vector
        except Exception as e:
            logger.error("❌ Error Detected", error=str(e), text=text[:50])
            raise e

    # Batch embedding
    def embed_batch(self, texts: list):
        vectors = []
        for text in texts:
            vectors.append(self.embed(text))
        return vectors