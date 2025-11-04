from src.processing.cleaner import clean_text
from src.processing.deduper import dedupe_document
from src.processing.language_detector import detect_language
from src.chunking.chunker_engine import ChunkerEngine
from src.embedding.embedding_engine import EmbeddingEngine

# === Mock du client d'embedding ===
class MockEmbeddingClient:
    def get_embedding(self, text, model):
        # renvoie un vecteur simulé, longueur = 1536 par défaut
        return [float(len(text) % 10)] * 1536

# === Exemple de texte trilingue ===
sample_text = """
🇫🇷 Version entretien technique (FR) : Processing
L’étape de processing applique des transformations métier aux textes validés pour garantir leur qualité avant le découpage. Le pipeline inclut le nettoyage, la détection de langue, la suppression des doublons et la validation du format. Chaque transformation est encapsulée dans un fichier dédié, et un worker orchestre le flux : il consomme les messages, applique les traitements, puis publie le message enrichi. Cette architecture modulaire assure des données propres, enrichies et prêtes pour le chunking, tout en maintenant une séparation nette entre logique métier et orchestration.

🇫🇷 Version entretien technique – Collecte & Extraction
Après la collecte, les données brutes sont stockées dans MinIO. L’étape d’extraction s’appuie sur des fichiers métiers spécialisés pour traiter les PDF, les URLs et les réponses API. Chaque contenu est transformé en un schéma JSON homogène, puis réinjecté dans un bucket dédié au processing. L’orchestration est assurée par extract_worker.py, qui hérite de BaseWorker pour gérer la réception des messages via RabbitMQ, appeler les extracteurs métiers, et publier les résultats. Le tout est instrumenté avec du logging structuré et des métriques Prometheus, garantissant traçabilité, observabilité et scalabilité.

🇫🇷 Résumé Embedding & Vector DB
Les chunks sont transformés en vecteurs numériques (embeddings) pour capturer leur sens, puis stockés dans une base vectorielle (Milvus) pour un accès rapide et indexable. Chaque vecteur conserve ses métadonnées (id, ordre, contenu, langue) et les opérations sont validées et surveillées via des métriques. L’orchestration (queue, retries, logs) reste séparée de la logique métier.

Le Retrieval Layer transforme les requêtes utilisateurs en contexte structuré pour le LLM. Il commence par classifier la requête (lexicale, sémantique, factuelle, contextuelle) et oriente vers les retrievers appropriés (Milvus pour sémantique, Elasticsearch pour lexical, ou hybride). Les résultats sont normalisés et fusionnés par le Ranker, puis raffinés par le Re-Ranker, qui peut utiliser différents modèles selon le type de requête pour maximiser la pertinence. Enfin, le Context Builder agrège les chunks, gère les métadonnées et la limite de tokens pour produire un contexte exploitable par le LLM. Cette architecture garde la vector DB et le moteur lexical séparés, et prépare les données pour le repo LLM Integration sans lier les deux.
"""

def main():
    # Clean
    cleaned = clean_text(sample_text)
    print("✅ Texte nettoyé :")
    print(cleaned[:200], "...")  # aperçu
    print("-" * 80)

    # Dedupe
    deduped = dedupe_document(cleaned)
    print("✅ Texte dédupliqué :")
    print(deduped[:200], "...")
    print("-" * 80)

    # Dtect language
    language = detect_language(deduped)
    print(f"✅ Langue détectée : {language}")
    print("-" * 80)

    # Chunking
    chunk_config = {
        "strategy": "by_tokens",  # ou "by_tokens", "by_paragraph"
        "max_tokens": 128,
        "overlap": 20
    }
    chunker = ChunkerEngine(chunk_config)
    chunks = chunker.chunk(deduped)

    print(f"✅ Chunking terminé ({len(chunks)} chunks produits) :")
    for i, chunk in enumerate(chunks[:5], start=1):
        print(f"Chunk {i}: {chunk['content'][:100]}...")
    print("-" * 80)

    # Embedding (mock)
    embedding_config = {
        "model": "mock-model",
        "dimension": 1536,
        "batch_size": 32
    }
    embedding_engine = EmbeddingEngine(embedding_config, model_client=MockEmbeddingClient())

    embeddings = []
    for chunk in chunks:
        content = chunk.get("content", "")
        vector = embedding_engine.embed(content)
        embeddings.append(vector)

    print(f"✅ Embedding terminé pour {len(embeddings)} chunks")
    for i, vec in enumerate(embeddings[:3], start=1):
        print(f"Chunk {i} vector (aperçu 10 premières valeurs) : {vec[:10]}")

if __name__ == "__main__":
    main()