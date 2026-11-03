# Estrategia de Testing

Para garantizar que el sistema RAG sea robusto y no dependa de servicios externos (que pueden fallar o generar costos), implementamos una estrategia de testing en capas:

## 1. Unit Tests (Pruebas Unitarias)
*   **Configuración:** `test_config.py` verifica que las variables de entorno se carguen correctamente.
*   **Fábricas:** `test_llm_factory.py` y `test_embeddings_factory.py` prueban el Patrón Registry, asegurando que cada proveedor devuelva la instancia correcta y que los errores se manejen adecuadamente.

## 2. Integration Tests (Pruebas de Integración)
*   **RAG Engine:** `test_rag_engine.py` mockea el LLM y la base de datos vectorial para probar la lógica de extracción de fuentes, cálculo de tokens y formateo de contexto.
*   **API Endpoints:** `test_main.py` usa `TestClient` de FastAPI para simular peticiones HTTP, verificando respuestas exitosas (200) y manejo de errores (500).

## 3. Mocking Strategy (Estrategia de Simulación)
No realizamos llamadas reales a las APIs de Groq o OpenRouter durante los tests. Usamos `unittest.mock` para:
*   Simular respuestas del LLM con `AIMessage`.
*   Simular metadatos de tokens (`usage_metadata`).
*   Simular documentos recuperados de ChromaDB.

Esto garantiza que los tests sean **rápidos, gratuitos y deterministas**.

## 4. Cobertura
Utilizamos `pytest-cov` para medir la cobertura. El objetivo es mantener un **100% en la carpeta `app/`**, excluyendo los scripts de ingesta y evaluación (que son de un solo uso).