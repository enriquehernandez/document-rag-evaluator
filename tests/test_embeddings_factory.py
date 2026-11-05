import pytest
from unittest.mock import patch
from app.core.embeddings_factory import get_embeddings
from app.core.config import settings

# Prueba la fábrica de embeddings.


@patch("app.core.embeddings_factory.OpenAIEmbeddings")
def test_get_embeddings_openrouter(mock_openai_emb):
    settings.EMBEDDING_PROVIDER = "OPENROUTER"
    get_embeddings()
    mock_openai_emb.assert_called_once()


def test_get_embeddings_invalid_provider():
    settings.EMBEDDING_PROVIDER = "INVALID"
    with pytest.raises(ValueError, match="Proveedor de Embeddings no soportado"):
        get_embeddings()


def test_get_embeddings_openrouter_missing_key():
    settings.EMBEDDING_PROVIDER = "OPENROUTER"
    settings.OPENROUTER_API_KEY = ""  # Simulamos que falta la llave
    with pytest.raises(ValueError, match="Se requiere OPENROUTER_API_KEY"):
        get_embeddings()


@patch("langchain_huggingface.HuggingFaceEmbeddings")
def test_get_embeddings_huggingface(mock_hf):
    settings.EMBEDDING_PROVIDER = "HUGGINGFACE"
    get_embeddings()
    mock_hf.assert_called_once()
