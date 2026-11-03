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
- **Registry Pattern (Factory Mejorado):** Utilizado en `llm_factory.py` y `embeddings_factory.py`. En lugar de una cadena de `if/elif` (que viola el principio Open/Closed de SOLID), usamos un diccionario (`_PROVIDER_REGISTRY`) que mapea el nombre del proveedor a su función constructora. Agregar un nuevo proveedor solo requiere crear una función y añadir una línea al diccionario, sin modificar la lógica central.
- **LCEL (LangChain Expression Language):** Uso de tuberías (`|`) para construir la cadena de ejecución de forma declarativa.