# Architecture Design

## 1. Diagrama de Flujo (Data Pipeline)
```mermaid
graph TD
    A[Usuario] -->|Pregunta| B(FastAPI Endpoint)
    B --> C{RAG Engine}
    C -->|Búsqueda Semántica| D[(ChromaDB)]
    D -->|Retorna Contexto| C
    C -->|Prompt + Contexto| E[LLM Factory]
    E -->|Genera Respuesta| F[LLM: Groq / OpenAI / Claude]
    F -->|Respuesta + Citas| B
    B -->|JSON| A
```

## 2. Flujo de Ingesta (Offline)
```mermaid
sequenceDiagram
    participant Dev as Desarrollador
    participant Script as scripts/ingest.py
    participant PDF as Carpeta /data
    participant API as OpenRouter (Embeddings)
    participant DB as ChromaDB

    Dev->>Script: Ejecuta ingesta
    Script->>PDF: Lee archivos PDF
    Script->>Script: Divide en chunks (1000 chars)
    Script->>API: Envía texto para Embeddings
    API-->>Script: Retorna Vectores
    Script->>DB: Guarda Vectores + Texto
    Script-->>Dev: ¡Ingesta Exitosa!
```

## 3. Componentes de Software
- **API Layer:** FastAPI (endpoints asíncronos y documentados con Swagger).
- **Ingestion Layer:** Script de Python que extrae texto de PDFs (`PyPDFLoader`) y los divide (`RecursiveCharacterTextSplitter`).
- **Vector Store:** ChromaDB (base de datos local persistente).
- **Embeddings:** Generados vía OpenRouter (`openai/text-embedding-3-small`).
- **LLM Provider:** Groq (`llama-3.3-70b-versatile`) configurado para respuestas ultrarrápidas.

## 4. Patrones de Diseño Aplicados
- **Factory Pattern:** Utilizado en `llm_factory.py` y `embeddings_factory.py` permiten cambiar de proveedor de IA sin modificar la lógica del RAG según el archivo `.env`.
- **LCEL (LangChain Expression Language):** Uso de tuberías (`|`) para construir la cadena de ejecución de forma declarativa.