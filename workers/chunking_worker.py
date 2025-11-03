# src/workers/chunker_worker.py
from workers.base_worker import BaseWorker
from src.chunking.chunker_engine import ChunkerEngine
from src.core.config_loader import load_config
from logs.logger import logger
from metrics.monitoring import increment_chunks

class ChunkerWorker(BaseWorker):
    """
    Worker qui découpe les messages déjà prétraités en chunks.
    Pipeline : Cleaned/validated text → ChunkEngine → enrichissement message
    """
    input_queue = "processed_messages"    # queue provenant du ProcessWorker
    output_queue = "chunked_messages"     # queue pour l'étape suivante
    worker_name = "ChunkerWorker"

    def __init__(self, config_path="chunker/chunker_config.yaml"):
        super().__init__(worker_name=self.worker_name)
        self.config = load_config(config_path)
        self.engine = ChunkerEngine(self.config)

    def process_message(self, msg: dict):
        message_id = msg.get("id")
        text = msg.get("text", "")

        if not text.strip():
            logger.warning("Message vide reçu pour chunking", message_id=message_id)
            return None

        # --- 1️⃣ Chunking via le moteur ---
        chunks = self.engine.chunk(text)

        # --- 2️⃣ Enrichissement du message ---
        msg["chunks"] = chunks
        msg["num_chunks"] = len(chunks)

        # --- 3️⃣ Métriques ---
        increment_chunks(self.worker_name, len(chunks))

        # --- 4️⃣ Retourne le message enrichi pour publication ---
        return msg