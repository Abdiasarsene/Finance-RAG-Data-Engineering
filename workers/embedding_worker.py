# workers/embedding_worker.py
from workers.base_worker import BaseWorker
from src.embedding.embedding_engine import EmbeddingEngine
from src.core.config_loader import load_config
from logs.logger import logger
from metrics.monitoring import increment_messages, observe_processing_time, increment_errors, embedding_chunks_processed, Gauge

# # embedding metrics
# embedding_chunks_processed = Gauge(
#     "embedding_chunks_processed",
#     "Number of chunks embedded per worker",
#     ["worker"]
# )

# ====== EMBEDDING WORKER ======
class EmbeddingWorker(BaseWorker):
    # Set up
    input_queue = "chunked_messages"
    output_queue = "embedded_messages"
    worker_name = "EmbeddingWorker"

    def __init__(self, config_path="src/embedding/configs/embedding_config.yaml", model_client=None):
        super().__init__(worker_name=self.worker_name)
        self.config = load_config(config_path)
        self.engine = EmbeddingEngine(self.config, model_client=model_client)

    # Wrap message
    def process_message(self, msg: dict):
        message_id = msg.get("id")
        chunks = msg.get("chunks", [])

        if not chunks:
            logger.warning("No chunk found for embedding", message_id=message_id)
            return None

        vectors = []
        try:
            for chunk in chunks:
                vector = self.engine.embed(chunk["content"])
                vectors.append(vector)
            msg["embeddings"] = vectors
            msg["num_embeddings"] = len(vectors)

            # metrics
            embedding_chunks_processed.labels(worker=self.worker_name).set(len(vectors))
        except Exception as e:
            increment_errors(self.worker_name, error_type="embedding_error")
            logger.error("Erreur lors de l'embedding d'un chunk", message_id=message_id, error=str(e))
            return None

        return msg