# 🧠 Advanced RAG Evaluator

Un sistema de Generación Aumentada por Recuperación (RAG) de nivel producción, diseñado para consultar documentos PDF (ej. contratos, manuales técnicos, guías) con un alto grado de precisión y trazabilidad.

Este proyecto va un paso más allá del RAG básico, incorporando **mecanismos de evaluación automatizada** (Ragas), **arquitectura agnóstica al proveedor de IA** y una **API REST moderna** que devuelve fuentes auditables y consumo de tokens.

## ✨ Características Principales

- **Arquitectura Provider-Agnostic (Multi-IA):** Capacidad de cambiar entre OpenAI, Anthropic (Claude), Google (Gemini), Groq y OpenRouter simplemente modificando una variable de entorno (Patrón Factory).
- **Búsqueda Vectorial Eficiente:** Uso de ChromaDB para almacenamiento y búsqueda semántica local.
- **API REST Moderna:** Endpoints asíncronos documentados automáticamente con FastAPI y Swagger UI, con soporte para LCEL (LangChain Expression Language).
- **Trazabilidad Completa:** La API devuelve la respuesta, las fuentes citadas (nombre del PDF y página) y el desglose de tokens consumidos (`prompt_tokens`, `completion_tokens`, `total_tokens`).
- **Evaluación Continua (Ragas):** Pipeline integrado (en desarrollo) para medir métricas clave como *Faithfulness*, *Answer Relevance* y *Context Precision*.
- **Gestión de Dependencias:** Utiliza `uv` para una resolución e instalación de paquetes ultrarrápida y reproducible.

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.11 (Recomendado para compatibilidad con el ecosistema de IA)
- **Backend Framework:** FastAPI + Uvicorn
- **Orquestación de IA:** LangChain (usando LCEL)
- **Vector Database:** ChromaDB
- **Embeddings:** OpenRouter (`openai/text-embedding-3-small`)
- **Evaluación de IA:** Ragas
- **Gestor de Paquetes:** uv

## 🏗️ Arquitectura y Estructura del Proyecto

El proyecto sigue una estructura de *Product Blueprint* (Docs-as-Code) y patrones de diseño como *Factory* para garantizar la escalabilidad.

```text
📁 document-rag-evaluator/
├── 📁 PRODUCT_BLUEPRINT/       # Documentación técnica del proyecto
│   ├── 00_FOUNDATION/          # Problema, visión y glosario
│   ├── 01_DESIGN_SYSTEM/       # Arquitectura y diagramas Mermaid
│   ├── 02_COMPONENTS/          # Contratos técnicos de la lógica RAG
│   └── 03_SECURITY_AND_AUDIT/  # Políticas de seguridad y evaluación (Ragas)
│
├── 📁 app/                     # Código fuente principal
│   ├── core/                   # Configuración y Fábricas de LLMs/Embeddings
│   ├── services/               # Lógica de RAG (LangChain)
│   └── main.py                 # Endpoints de FastAPI
│
├── 📁 data/                    # Directorio para colocar los PDFs
├── 📁 scripts/                 # Scripts ejecutables (ingest.py, evaluate.py)
├── .env.example                # Plantilla de variables de entorno
├── pyproject.toml              # Dependencias gestionadas por uv
└── README.md                   # Este archivo
```

Para más detalles sobre la arquitectura, consulta el [Product Blueprint](PRODUCT_BLUEPRINT/README.md).

## 🚀 Quick Start
Este proyecto utiliza `uv` para la gestión de dependencias y entornos virtuales, lo que garantiza una configuración ultrarrápida.

1. Requisitos Previos
Instala uv si aún no lo tienes:

```bash
# En macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# En Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Nota: Si acabas de instalarlo, reinicia tu terminal o ejecuta source $HOME/.local/bin/env.
source $HOME/.local/bin/env
```

2. Configuración del Entorno
Clona el repositorio e instala las dependencias exactas (esto creará el entorno virtual `.venv` y el archivo `uv.lock`):

```bash
git clone https://github.com/enriquehernandez/document-rag-evaluator.git
cd rag-evaluator
uv sync
```

2.1 Fija la versión de Python (opcional pero recomendado):

```bash
# Si quieres usar 3.11 en lugar de la 3.13
uv python pin 3.11
```

3. Variables de Entorno
Copia el archivo de ejemplo y configura tus API Keys. Por defecto, el proyecto está configurado para usar OpenRouter.

```bash
cp .env.example .env
```

Edita el archivo .env y define el proveedor que deseas usar:

```env
# Opciones: OPENAI, CLAUDE, GEMINI, GROQ, OPENROUTER
LLM_PROVIDER=GROQ
GROQ_API_KEY=tu_api_key_de_groq
GROQ_MODEL=llama-3.3-70b-versatile

EMBEDDING_PROVIDER=OPENROUTER
OPENROUTER_API_KEY=tu_api_key_de_openrouter
OPENROUTER_EMBEDDING_MODEL=openai/text-embedding-3-small
```

4. Ingesta de Documentos

- Coloca uno o más archivos PDF dentro de la carpeta data/.
- Ejecuta el script de ingesta para leer los PDFs, generar los embeddings y guardarlos en ChromaDB:

```bash
uv run python scripts/ingest.py
```
(Deberías ver un mensaje de éxito y se creará la carpeta chroma_db/).

5. Levantar el Servidor
Inicia la API de FastAPI:

```bash
uv run uvicorn app.main:app --reload
```

Accede a la documentación interactiva de la API (Swagger UI) en: http://127.0.0.1:8000/docs

## 📡 Ejemplo de Respuesta de la API
Al hacer un POST al endpoint /chat con la siguiente pregunta:
```json
{
  "query": "¿Cuáles son los requisitos para la visa?"
}
```

La API devuelve un JSON estructurado para auditoría y control de costos:
```json
{
  "answer": "Según el documento, los requisitos son...",
  "sources": [
    "Guia_para_nuevos_inmigrantes_M-618_sp.pdf (pág. 12)",
    "International Express Intermediate 3rd Edition.pdf (pág. 5)"
  ],
  "tokens_used": {
    "prompt_tokens": 1450,
    "completion_tokens": 85,
    "total_tokens": 1535
  }
}
```

## 🧪 Testing y Calidad de Código

El proyecto cuenta con una suite de pruebas unitarias y de integración utilizando **pytest**. Se ha alcanzado un **100% de cobertura de código** en la carpeta `app/`, asegurando la fiabilidad de la API, las fábricas de LLMs y el motor RAG.

Para ejecutar los tests y ver el reporte de cobertura:
```bash
uv run pytest --cov=app tests/ --cov-report=term-missing
o
uv run tom test
```

**Herramientas utilizadas:**

- pytest y pytest-asyncio para pruebas síncronas y asíncronas.
- unittest.mock para simular APIs externas (Groq, OpenRouter) y evitar costos durante los tests.
- SonarQube (análisis estático) para garantizar que no haya complejidad cognitiva excesiva.

## 📊 Evaluación de Calidad (Ragas)
El proyecto incluye un pipeline de evaluación automatizado para medir la calidad de las respuestas y evitar alucinaciones. Utiliza el LLM configurado como "juez" para auditar los resultados.

Para ejecutar la evaluación:
```bash
uv run python scripts/evaluate.py
```

🧑‍💻 Autor
Enrique Hernández Leiva
* [LinkedIn](https://www.linkedin.com/in/enrique-hernandez-leiva/)
* [GitHub](https://github.com/enriquehernandez)

