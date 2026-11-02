# 🧠 Advanced RAG Evaluator

Un sistema de Generación Aumentada por Recuperación (RAG) listo para producción, diseñado para consultar documentos PDF (ej. contratos, manuales técnicos) con un alto grado de precisión.

Este proyecto va un paso más allá del RAG básico, incorporando **mecanismos de evaluación automatizada** (Ragas) para medir la fidelidad y la relevancia de las respuestas generadas por el LLM, garantizando soluciones sin alucinaciones.

## ✨ Características Principales

- **Arquitectura Provider-Agnostic (Multi-IA):** Capacidad de cambiar entre OpenAI, Anthropic (Claude), Google (Gemini), Groq y OpenRouter simplemente modificando una variable de entorno.
- **Búsqueda Híbrida:** Combinación de búsqueda vectorial (ChromaDB) y búsqueda léxica (BM25) para maximizar la precisión del contexto recuperado.
- **Evaluación Continua (Ragas):** Pipeline integrado para medir métricas clave como *Faithfulness*, *Answer Relevance* y *Context Precision*.
- **API REST Moderna:** Endpoints asíncronos documentados automáticamente con FastAPI y Swagger UI.
- **Moderna Gestión de Dependencias:** Utiliza `uv` para una resolución e instalación de paquetes ultrarrápida.

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.11 / 3.12 (Recomendado)
- **Backend Framework:** FastAPI + Uvicorn
- **Orquestación de IA:** LangChain (usando LCEL - LangChain Expression Language)
- **Vector Database:** ChromaDB
- **Evaluación de IA:** Ragas
- **Gestor de Paquetes:** uv

## 🏗️ Arquitectura del Proyecto

El proyecto sigue una estructura de *Product Blueprint* (Docs-as-Code) y patrones de diseño como *Factory* para garantizar la escalabilidad y el desacoplamiento del código.

```text
├── PRODUCT_BLUEPRINT
│   ├── 00_FOUNDATION                   # Definición del problema y visión
│   │   └── 00_problem_statement.md     
│   ├── 01_DESIGN_SYSTEM                # Arquitectura y principios de diseño
│   │   └── 00_architecture.md          
│   ├── 02_COMPONENTS                   # Contratos técnicos de los componentes
│   │   └── 00_rag_chain_component.md   
│   ├── 07_AUDIT_AND_IMPROVEMENTS
│   │   └── 00_evaluation_plan.md
│   └── README.md
├── README.md
├── app                                 # Código fuente principal
│   ├── core                            # Configuración y Fábrica de LLMs
│   │   ├── config.py
│   │   └── llm_factory.py
│   ├── main.py                         # Puntos de entrada de FastAPI
│   └── services                        # Lógica de RAG (LangChain)
│       └── rag_engine.py
└── requirements.txt
```

## 🚀 Quick Start
Este proyecto utiliza uv para la gestión de dependencias, lo que garantiza una configuración ultrarrápida.

1. Requisitos Previos
Instala uv si aún no lo tienes:

```bash
# En macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# En Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Para que reconozca el comando uv
source $HOME/.local/bin/env
```

2. Configuración del Entorno
Clona el repositorio e instala las dependencias (esto creará automáticamente el entorno virtual y el archivo uv.lock):

```bash
git clone https://github.com/tu-usuario/rag-evaluator.git
cd rag-evaluator
uv sync
```

2.1 Fija la versión de Python (opcional pero recomendado):

```bash
# Si quieres usar 3.11 en lugar de la 3.13
uv python pin 3.11
```

2.2 Agrega las dependencias:

```bash
# uv resolverá e instalará todo mucho más rápido que pip
uv add fastapi uvicorn langchain langchain-openai langchain-anthropic langchain-google-genai langchain-groq chromadb ragas pypdf python-dotenv pydantic-settings rank_bm25
```

3. Variables de Entorno
Copia el archivo de ejemplo y configura tus API Keys. Por defecto, el proyecto está configurado para usar OpenRouter.

```bash
cp .env.example .env
```

Edita el archivo .env y define el proveedor que deseas usar:

```env
# Opciones: OPENAI, CLAUDE, GEMINI, GROQ, OPENROUTER
LLM_PROVIDER=OPENROUTER
OPENROUTER_API_KEY=tu_api_key_aqui
```

4. Ingesta de Documentos
Coloca tus archivos PDF en la carpeta /data y ejecuta el script de ingesta para generar los embeddings en ChromaDB:

```bash
uv run python scripts/ingest.py
```

5. Levantar el Servidor
Inicia la API de FastAPI:

```bash
uv run uvicorn app.main:app --reload
```

Accede a la documentación interactiva de la API (Swagger UI) en: http://127.0.0.1:8000/docs

### Quick Start Resume

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

1. Install uv (if you haven't already):
   `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. Sync dependencies (creates venv and installs everything):
   `uv sync`

3. Run the API:
   `uv run uvicorn app.main:app --reload`

## 📊 Evaluación de Calidad (Ragas)
(Sección en desarrollo)
Una vez ingeridos los documentos, puedes correr el pipeline de evaluación para verificar la calidad de las respuestas:

```bash
uv run python scripts/evaluate.py
```

🧑‍💻 Autor
Enrique Hernández Leiva
* LinkedIn
* GitHub

