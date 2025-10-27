# src/workers/process_worker.py
from workers.base_worker import BaseWorker
from src.processing.cleaner import clean_text
from src.processing.deduper import dedupe_document
from src.processing.language_detector import detect_language
from json_container.json_validator import validate_json

class ProcessWorker(BaseWorker):
    """
    Worker qui traite les messages validés par CollectDataWorker.
    Pipeline : cleaner → language detection → deduper
    """
    input_queue = "validated_messages"   # queue provenant de CollectDataWorker
    output_queue = "processed_messages"  # queue finale ou suivante
    worker_name = "ProcessWorker"

    def __init__(self, dedupe_threshold: float = 0.8):
        super().__init__(worker_name=self.worker_name)
        self.dedupe_threshold = dedupe_threshold  # paramètre spécifique

    def process_message(self, msg: dict):
        message_id = msg.get("id")

        # --- 1️⃣ Validation supplémentaire si besoin ---
        if not validate_json(msg, message_id=message_id):
            # Message invalide → skip
            return None

        # --- 2️⃣ Nettoyage ---
        text = clean_text(msg.get("text"), message_id=message_id)

        # --- 3️⃣ Détection de langue ---
        lang = detect_language(text, message_id=message_id)
        msg["lang"] = lang

        # --- 4️⃣ Deduplication ---
        deduped_text = dedupe_document(text, message_id=message_id)
        msg["text"] = deduped_text

        # --- 5️⃣ Retourne le message traité pour publication ---
        return msg