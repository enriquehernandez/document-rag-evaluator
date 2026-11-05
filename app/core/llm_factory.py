from typing import Callable, Dict
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from app.core.config import settings


def _build_openrouter() -> BaseChatModel:
    return ChatOpenAI(
        model=settings.OPENROUTER_MODEL,
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )


def _build_openai() -> BaseChatModel:
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0,
    )


def _build_claude() -> BaseChatModel:
    return ChatAnthropic(
        model=settings.CLAUDE_MODEL,
        api_key=settings.CLAUDE_API_KEY,
        temperature=0,
    )


def _build_gemini() -> BaseChatModel:
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0,
    )


def _build_groq() -> BaseChatModel:
    return ChatGroq(
        model=settings.GROQ_MODEL,
        api_key=settings.GROQ_API_KEY,
        temperature=0,
        max_tokens=4096,  # Mantenemos tu configuración de margen
        n=1               # Mantenemos el n=1 para evitar errores
    )


# ==========================================
# REGISTRY PATTERN
# Diccionario que mapea el string del proveedor a su función constructora
# ==========================================
_PROVIDER_REGISTRY: Dict[str, Callable[[], BaseChatModel]] = {
    "OPENROUTER": _build_openrouter,
    "OPENAI": _build_openai,
    "CLAUDE": _build_claude,
    "GEMINI": _build_gemini,
    "GROQ": _build_groq,
}


def get_llm() -> BaseChatModel:
    """
    Factory Pattern (Registry): Retorna una instancia del LLM según la variable LLM_PROVIDER.

    Todos los modelos seleccionados deben soportar Vision y Tool Calling.
    """
    provider = settings.LLM_PROVIDER.upper()
    print(f"🤖 [LLM FACTORY] Inicializando proveedor: {provider}")

    builder = _PROVIDER_REGISTRY.get(provider)

    if not builder:
        raise ValueError(
            f"Proveedor no soportado: {provider}. "
            f"Usa uno de los siguientes: {', '.join(_PROVIDER_REGISTRY.keys())}"
        )

    return builder()
