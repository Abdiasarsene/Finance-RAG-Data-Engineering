# src/workers/vector_store_worker.py
from workers.base_worker import BaseWorker
from connectors.milvus.milvus_connection import MilvusConnection
from src.vector_store.vector_store_engine import VectorStoreEngine
from logs.logger import logger
from metrics.monitoring import set_vector_store_queue_size

class VectorStoreWorker(BaseWorker):
    """
    Worker qui stocke les embeddings dans Milvus.
    Pipeline : embeddings → validation → insertion batch dans Milvus
    """
    input_queue = "embedded_messages"
    output_queue = None  # Pas de queue suivante pour ce worker
    worker_name = "VectorStoreWorker"

    def __init__(self, config_path="vector_store/vector_store_config.yaml"):
        super().__init__(worker_name=self.worker_name)
        self.milvus_conn = MilvusConnection(config_path)
        self.engine = VectorStoreEngine(self.milvus_conn)

    def process_message(self, msg: dict):
        message_id = msg.get("id")
        embeddings = msg.get("embeddings", [])
        chunks = msg.get("chunks", [])

        if not embeddings or not chunks:
            logger.warning("Aucun embedding ou chunk pour insertion", message_id=message_id)
            return None

        # Préparer les vecteurs à insérer
        vectors_to_insert = []
        for i, chunk in enumerate(chunks):
            try:
                vectors_to_insert.append({
                    "vector": embeddings[i],
                    "chunk_id": chunk.get("chunk_id"),
                    "message_id": message_id,
                    "content": chunk.get("content"),
                    "order": chunk.get("order"),
                    "lang": msg.get("lang", "unknown")
                })
            except IndexError:
                logger.error("Mismatch embeddings/chunks", message_id=message_id)
                continue

        # Mettre à jour la métrique de queue size
        set_vector_store_queue_size(self.worker_name, len(vectors_to_insert))

        # Insertion batch via le moteur
        inserted_count = self.engine.insert_batch(vectors_to_insert, worker_name=self.worker_name)

        logger.info(
            "Message inséré dans Milvus",
            message_id=message_id,
            inserted_count=inserted_count
        )

        # Pas de sortie → on ne publie rien
        return None