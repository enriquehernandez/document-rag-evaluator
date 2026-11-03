from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
import pytest

# Prueba los endpoints de FastAPI usando TestClient.

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@patch("app.main.rag_engine")
def test_chat_endpoint(mock_rag_engine):
    # Simular la respuesta asíncrona del motor
    mock_rag_engine.get_answer_with_sources = MagicMock()

    # Simulamos el retorno usando un mock asíncrono
    async def mock_async_response(query):
        return {
            "answer": "Respuesta de prueba",
            "sources": ["doc.pdf (pág. 1)"],
            "tokens_used": {"total_tokens": 20, "prompt_tokens": 10, "completion_tokens": 10},
            "metadata": {"latency_seconds": 1.5, "chunks_retrieved": 1}
        }

    mock_rag_engine.get_answer_with_sources.side_effect = mock_async_response

    response = client.post("/chat", json={"query": "Hola"})

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Respuesta de prueba"
    assert data["sources"] == ["doc.pdf (pág. 1)"]
    assert data["tokens_used"]["total_tokens"] == 20


@patch("app.main.rag_engine")
def test_chat_endpoint_error_500(mock_rag_engine):
    # Simulamos que el motor RAG falla
    mock_rag_engine.get_answer_with_sources.side_effect = Exception(
        "Error simulado")

    response = client.post("/chat", json={"query": "Hola"})

    assert response.status_code == 500
    assert response.json()["detail"] == "Error interno procesando la solicitud"
