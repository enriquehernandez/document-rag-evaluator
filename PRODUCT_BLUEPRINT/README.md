# 🧠 Advanced RAG Evaluator

Un sistema de Generación Aumentada por Recuperación (RAG) diseñado para consultar documentos PDF (ej. contratos, manuales técnicos) con un alto grado de precisión. 

Este proyecto va un paso más allá del RAG básico, incorporando **mecanismos de evaluación automatizada** (Ragas) para medir la fidelidad (Faithfulness) y la relevancia de las respuestas generadas por el LLM, garantizando soluciones listas para producción.

## 🚀 Características Principales
- **Ingesta Inteligente:** Chunking semántico de documentos PDF.
- **Búsqueda Híbrida:** Combinación de búsqueda vectorial (ChromaDB) y búsqueda por palabras clave (BM25) para máxima precisión.
- **LLMs Soportados:** Azure OpenAI, OpenAI o modelos locales vía Ollama (configurable).
- **Evaluación Continua:** Pipeline automatizado con la librería `Ragas` para medir alucinaciones y relevancia.
- **API REST:** Endpoints documentados con FastAPI y Swagger.

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.11+
- **Backend:** FastAPI, Uvicorn
- **Orquestación de IA:** LangChain
- **Base de Datos Vectorial:** ChromaDB
- **Evaluación:** Ragas
- **Frontend (Opcional):** Streamlit (para demo rápida)

## ⚙️ Instalación y Uso
1. Clona el repositorio.
2. Crea un entorno virtual: `python -m venv venv`
3. Activa el entorno e instala dependencias: `pip install -r requirements.txt`
4. Copia el archivo `.env.example` a `.env` y configura tus API Keys.
5. Coloca tus PDFs en la carpeta `/data`.
6. Ejecuta la API: `uvicorn app.main:app --reload`

## 📊 Evaluación
*(Aquí pondrás una captura de pantalla de los resultados de Ragas una vez que lo implementes)*