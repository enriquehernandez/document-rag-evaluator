from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from app.core.config import settings


def get_llm() -> BaseChatModel:
    """
    Retorna una instancia del LLM configurado en el archivo .env
    """
    provider = settings.LLM_PROVIDER.upper()

    if provider == "OPENAI":
        return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            temperature=0
        )

    elif provider == "CLAUDE":
        return ChatAnthropic(
            api_key=settings.CLAUDE_API_KEY,
            model=settings.CLAUDE_MODEL,
            temperature=0
        )

    elif provider == "GEMINI":
        return ChatGoogleGenerativeAI(
            google_api_key=settings.GEMINI_API_KEY,
            model=settings.GEMINI_MODEL,
            temperature=0
        )

    elif provider == "GROQ":
        return ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL,
            temperature=0
        )

    elif provider == "OPENROUTER":
        # OpenRouter usa la interfaz de OpenAI pero apuntando a su URL
        return ChatOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            model=settings.OPENROUTER_MODEL,
            base_url="https://openrouter.ai/api/v1",
            temperature=0
        )

    else:
        raise ValueError(f"Proveedor de LLM no soportado: {provider}")
