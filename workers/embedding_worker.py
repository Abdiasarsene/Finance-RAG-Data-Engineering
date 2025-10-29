# src/workers/embedding_worker.py
from workers.base_worker import BaseWorker
from src.embedding.embedding_engine import EmbeddingEngine
from src.embedding.config_loader import load_chunker_config
from logs.logger import logger
from metrics.monitoring import increment_messages, observe_processing_time, increment_errors, Gauge

# métrique spécifique pour l'embedding
embedding_chunks_processed = Gauge(
    "embedding_chunks_processed",
    "Number of chunks embedded per worker",
    ["worker"]
)

class EmbeddingWorker(BaseWorker):
    """
    Worker qui transforme les chunks en vecteurs numériques (embeddings).
    Pipeline : chunks prétraités → embedding → ajout dans message
    """
    input_queue = "chunked_messages"
    output_queue = "embedded_messages"
    worker_name = "EmbeddingWorker"

    def __init__(self, config_path="embedding/embedding_config.yaml", model_client=None):
        super().__init__(worker_name=self.worker_name)
        self.config = load_chunker_config(config_path)
        self.engine = EmbeddingEngine(self.config, model_client=model_client)

    def process_message(self, msg: dict):
        message_id = msg.get("id")
        chunks = msg.get("chunks", [])

        if not chunks:
            logger.warning("Aucun chunk trouvé pour embedding", message_id=message_id)
            return None

        vectors = []
        try:
            for chunk in chunks:
                vector = self.engine.embed(chunk["content"])
                vectors.append(vector)
            msg["embeddings"] = vectors
            msg["num_embeddings"] = len(vectors)

            # métriques
            embedding_chunks_processed.labels(worker=self.worker_name).set(len(vectors))
        except Exception as e:
            increment_errors(self.worker_name, error_type="embedding_error")
            logger.error("Erreur lors de l'embedding d'un chunk", message_id=message_id, error=str(e))
            return None

        return msg