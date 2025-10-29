# src/embedding/embedding_engine.py
from logs.logger import logger
import time

class EmbeddingEngine:
    """
    Engine pour transformer des chunks de texte en vecteurs numériques.
    Encapsule le modèle d'embedding choisi.
    """
    def __init__(self, config: dict, model_client=None):
        self.model_name = config.get("model", "text-embedding-3-small")
        self.dimension = config.get("dimension", 1536)
        self.batch_size = config.get("batch_size", 32)
        # client externe pour le modèle (OpenAI, HuggingFace, etc.)
        self.model_client = model_client

    def embed(self, text: str):
        """
        Embedding d'un chunk unique.
        """
        if not text.strip():
            return [0.0] * self.dimension  # vecteur vide
        try:
            # Exemple simplifié : ici tu appellerais l'API de ton modèle
            vector = self.model_client.get_embedding(text, model=self.model_name)
            return vector
        except Exception as e:
            logger.error("Erreur lors de l'embedding", error=str(e), text=text[:50])
            raise e

    def embed_batch(self, texts: list):
        """
        Embedding en batch pour efficacité.
        """
        vectors = []
        for text in texts:
            vectors.append(self.embed(text))
        return vectors