from app.core.config import Settings

# Prueba que la configuración se cargue correctamente.


def test_settings_load_correctly():
    settings = Settings()
    assert settings.LLM_PROVIDER == "GROQ"
    assert settings.EMBEDDING_PROVIDER == "OPENROUTER"
    assert settings.GROQ_API_KEY == "fake-groq-key"
