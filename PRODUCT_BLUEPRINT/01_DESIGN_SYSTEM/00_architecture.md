# Architecture Design

## 1. Diagrama de Flujo (Data Pipeline)
[Usuario] -> (Pregunta) -> [FastAPI]
                            |
                            v
                    [LangChain Orchestrator]
                            |
            (Búsqueda Vectorial en ChromaDB)
                            |
                   (Contexto Relevante)
                            |
                            v
                    [LLM Factory (Groq/OpenAI)]
                            |
                            v
                    [Respuesta + Citas]

## 2. Componentes de Software
- **API Layer:** FastAPI (endpoints asíncronos y documentados con Swagger).
- **Ingestion Layer:** Script de Python que extrae texto de PDFs (`PyPDFLoader`) y los divide (`RecursiveCharacterTextSplitter`).
- **Vector Store:** ChromaDB (base de datos local persistente).
- **Embeddings:** Generados vía OpenRouter (`openai/text-embedding-3-small`).
- **LLM Provider:** Groq (`llama-3.3-70b-versatile`) configurado para respuestas ultrarrápidas.

## 3. Patrones de Diseño Aplicados
- **Factory Pattern:** Utilizado en `llm_factory.py` y `embeddings_factory.py` para instanciar el proveedor correcto según el archivo `.env`.
- **LCEL (LangChain Expression Language):** Uso de tuberías (`|`) para construir la cadena de ejecución de forma declarativa.