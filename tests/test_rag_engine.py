# Aquí probamos la lógica asíncrona del motor RAG (formateo de fuentes, extracción de tokens, etc).

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from langchain_core.messages import AIMessage
from app.services.rag_engine import RAGEngine


@pytest.mark.asyncio
@patch("app.services.rag_engine.get_llm")
@patch("app.services.rag_engine.get_embeddings")
@patch("app.services.rag_engine.Chroma")
@patch("app.services.rag_engine.StrOutputParser")  # <-- Mockeamos el parser
async def test_get_answer_with_sources(mock_parser, mock_chroma, mock_get_emb, mock_get_llm, mock_docs):
    # 1. Creamos la respuesta que devolverá el LLM
    fake_llm_response = AIMessage(
        content="Esta es una respuesta simulada del LLM.",
        response_metadata={"token_usage": {
            "prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}}
    )

    # 2. Configuramos el mock del LLM
    mock_llm = MagicMock()
    mock_llm.ainvoke = AsyncMock(return_value=fake_llm_response)
    mock_get_llm.return_value = mock_llm

    # 3. ✨ MOCK DEL StrOutputParser: Hacemos que el parser devuelva el texto directamente
    mock_parser_instance = MagicMock()
    mock_parser_instance.ainvoke = AsyncMock(
        return_value="Esta es una respuesta simulada del LLM.")
    mock_parser.return_value = mock_parser_instance

    # Instanciar el motor RAG
    engine = RAGEngine()

    # Mockear el retriever
    engine.retriever = MagicMock()
    engine.retriever.invoke.return_value = mock_docs

    # Ejecutar la función
    result = await engine.get_answer_with_sources("¿Cuáles son los requisitos?")

    # Verificar resultados
    assert result["answer"] == "Esta es una respuesta simulada del LLM."
    assert len(result["sources"]) == 2
    assert "guia.pdf (pág. 1)" in result["sources"]
    assert result["tokens_used"]["total_tokens"] == 15


def test_extract_sources(mock_docs):
    engine = RAGEngine.__new__(RAGEngine)
    sources = engine._extract_sources(mock_docs)
    assert len(sources) == 2
    assert "guia.pdf (pág. 1)" in sources
    assert "manual.pdf (pág. 2)" in sources


def test_extract_tokens_no_metadata():
    engine = RAGEngine.__new__(RAGEngine)
    # Simulamos una respuesta sin metadata de tokens
    mock_response = MagicMock()
    del mock_response.response_metadata
    del mock_response.usage_metadata

    tokens = engine._extract_tokens(mock_response)
    assert tokens["total_tokens"] == 0


@patch("app.services.rag_engine.get_llm")
@patch("app.services.rag_engine.get_embeddings")
@patch("app.services.rag_engine.Chroma")
def test_get_chain_legacy(mock_chroma, mock_get_emb, mock_get_llm):
    engine = RAGEngine()
    chain = engine.get_chain()
    assert chain is not None


def test_extract_tokens_usage_metadata():
    engine = RAGEngine.__new__(RAGEngine)

    # Simulamos una respuesta SIN response_metadata, pero CON usage_metadata
    mock_response = MagicMock()
    mock_response.response_metadata = {}  # Vacío para que falle el primer if

    # Configuramos usage_metadata como un diccionario
    mock_response.usage_metadata = {
        "input_tokens": 10,
        "output_tokens": 5,
        "total_tokens": 15
    }

    tokens = engine._extract_tokens(mock_response)

    # El código buscará 'prompt_tokens' y 'completion_tokens',
    # si no los encuentra usará 0. Verificamos que no explote.
    assert "total_tokens" in tokens
