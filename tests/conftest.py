import pytest
from unittest.mock import MagicMock

# Este archivo es vital. Aquí simulamos las variables de entorno para que los tests no dependan de tu archivo .env real.


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    # Simulamos las variables de entorno para que Pydantic no falle
    monkeypatch.setenv("LLM_PROVIDER", "GROQ")
    monkeypatch.setenv("GROQ_API_KEY", "fake-groq-key")
    monkeypatch.setenv("GROQ_MODEL", "llama3-70b-8192")
    monkeypatch.setenv("EMBEDDING_PROVIDER", "OPENROUTER")
    monkeypatch.setenv("OPENROUTER_API_KEY", "fake-openrouter-key")
    monkeypatch.setenv("OPENROUTER_EMBEDDING_MODEL",
                       "openai/text-embedding-3-small")


@pytest.fixture
def mock_llm():
    # Simula la respuesta de un LLM
    mock = MagicMock()
    mock.content = "Esta es una respuesta simulada del LLM."
    mock.response_metadata = {"token_usage": {
        "prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}}
    return mock


@pytest.fixture
def mock_docs():
    # Simula documentos recuperados de ChromaDB
    doc1 = MagicMock()
    doc1.page_content = "Contenido del documento 1 sobre requisitos."
    doc1.metadata = {"source": "/ruta/falsa/guia.pdf", "page": 1}

    doc2 = MagicMock()
    doc2.page_content = "Contenido del documento 2 sobre trámites."
    doc2.metadata = {"source": "/ruta/falsa/manual.pdf", "page": 2}
    return [doc1, doc2]
