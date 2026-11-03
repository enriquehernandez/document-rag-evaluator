import pytest
from unittest.mock import patch, MagicMock
from app.core.llm_factory import get_llm
from app.core.config import settings

# ==========================================
# 1. TESTS DE INTEGRACIÓN (Cubren las líneas rojas)
# Aquí probamos que las funciones _build_... funcionan
# ==========================================


@patch("app.core.llm_factory.ChatOpenAI")
def test_build_openrouter_integration(mock_chat_openai):
    settings.LLM_PROVIDER = "OPENROUTER"
    get_llm()  # Al no mockear el diccionario, entra a la función real
    mock_chat_openai.assert_called_once()


@patch("app.core.llm_factory.ChatOpenAI")
def test_build_openai_integration(mock_chat_openai):
    settings.LLM_PROVIDER = "OPENAI"
    get_llm()
    mock_chat_openai.assert_called_once()


@patch("app.core.llm_factory.ChatAnthropic")
def test_build_claude_integration(mock_chat_anthropic):
    settings.LLM_PROVIDER = "CLAUDE"
    get_llm()
    mock_chat_anthropic.assert_called_once()


@patch("app.core.llm_factory.ChatGoogleGenerativeAI")
def test_build_gemini_integration(mock_chat_gemini):
    settings.LLM_PROVIDER = "GEMINI"
    get_llm()
    mock_chat_gemini.assert_called_once()


@patch("app.core.llm_factory.ChatGroq")
def test_build_groq_integration(mock_chat_groq):
    settings.LLM_PROVIDER = "GROQ"
    get_llm()
    mock_chat_groq.assert_called_once()

# ==========================================
# 2. TESTS DEL REGISTRY (Lógica del diccionario)
# Verifican que get_llm busca bien en el diccionario
# ==========================================


@patch("app.core.llm_factory._PROVIDER_REGISTRY")
def test_get_llm_uses_registry(mock_registry):
    # Simulamos que el diccionario devuelve un mock
    mock_registry.get.return_value = MagicMock()

    settings.LLM_PROVIDER = "GROQ"
    get_llm()

    # Verificamos que se buscó la llave correcta
    mock_registry.get.assert_called_once_with("GROQ")

# ==========================================
# 3. TEST DE ERROR (Cubre el raise ValueError)
# ==========================================


def test_get_llm_invalid_provider():
    settings.LLM_PROVIDER = "INVALID_PROVIDER"
    with pytest.raises(ValueError, match="Proveedor no soportado"):
        get_llm()
