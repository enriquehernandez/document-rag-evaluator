from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings


def get_embeddings() -> Embeddings:
    """
    Retorna la instancia del modelo de embeddings configurado.
    """
    provider = settings.EMBEDDING_PROVIDER.upper()

    if provider == "OPENROUTER":
        if not settings.OPENROUTER_API_KEY:
            raise ValueError(
                "❌ Se requiere OPENROUTER_API_KEY para generar embeddings.")

        # Usamos el SDK de OpenAI, pero apuntando a la API de OpenRouter
        return OpenAIEmbeddings(
            api_key=settings.OPENROUTER_API_KEY,
            model=settings.OPENROUTER_EMBEDDING_MODEL,
            base_url="https://openrouter.ai/api/v1"  # <-- Aquí está la magia
        )

    elif provider == "HUGGINGFACE":
        # Importación perezosa (Lazy import) para no cargar Torch si no se usa
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name=settings.HUGGINGFACE_EMBEDDING_MODEL
        )

    else:
        raise ValueError(f"Proveedor de Embeddings no soportado: {provider}")
