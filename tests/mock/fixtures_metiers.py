import pytest

# Exemple de texte brut pour tests
@pytest.fixture
def sample_text():
    return "Voici un texte de test, avec des caractères spéciaux : éèê à ç !"

@pytest.fixture
def sample_text_multi_lang():
    return [
        "This is an English text.",
        "Ceci est un texte français.",
        "这是中文文本。"
    ]

@pytest.fixture
def sample_chunks():
    return [
        {"chunk_id": "c1", "content": "Premier chunk", "order": 1, "lang": "fr"},
        {"chunk_id": "c2", "content": "Second chunk", "order": 2, "lang": "fr"},
    ]

@pytest.fixture
def sample_vectors():
    # vecteurs factices pour tests vectorisation
    return [
        [0.1, 0.2, 0.3, 0.4],
        [0.4, 0.3, 0.2, 0.1],
    ]
