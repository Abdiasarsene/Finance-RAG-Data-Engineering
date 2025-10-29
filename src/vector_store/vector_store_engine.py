# src/vector_store/vector_store_engine.py
from logs.logger import logger
from metrics.monitoring import increment_vectors_inserted, increment_vector_store_errors, observe_vector_store_insert_time
import time

class VectorStoreEngine:
    def __init__(self, milvus_connection):
        self.collection = milvus_connection.collection
        self.batch_size = milvus_connection.batch_size

    def validate_vectors(self, vectors):
        # Vérifie que chaque vecteur a les champs nécessaires
        valid = []
        for v in vectors:
            if all(k in v for k in ("vector", "chunk_id", "message_id", "content", "order", "lang")):
                valid.append(v)
            else:
                logger.warning("Vecteur invalide", vector=v)
        return valid

    def insert_batch(self, vectors, worker_name="VectorStoreWorker"):
        vectors = self.validate_vectors(vectors)
        if not vectors:
            logger.warning("Aucun vecteur valide à insérer")
            return 0

        start_time = time.time()
        try:
            fields = {
                "vector": [v["vector"] for v in vectors],
                "chunk_id": [v["chunk_id"] for v in vectors],
                "message_id": [v["message_id"] for v in vectors],
                "content": [v["content"] for v in vectors],
                "order": [v["order"] for v in vectors],
                "lang": [v["lang"] for v in vectors]
            }
            self.collection.insert(fields)
            duration = time.time() - start_time
            observe_vector_store_insert_time(worker_name, duration)
            increment_vectors_inserted(worker_name, len(vectors))
            logger.info("Insertion batch réussie", count=len(vectors), duration=duration)
            return len(vectors)
        except Exception as e:
            increment_vector_store_errors(worker_name, error_type="insert_error")
            logger.error("Erreur insertion batch Milvus", error=str(e))
            return 0