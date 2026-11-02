
# Evaluation Plan (Ragas)

Para asegurar que el sistema está listo para producción, implementaremos un pipeline de evaluación automatizado utilizando la librería **Ragas**.

## Dataset de Evaluación
Crearemos un set de preguntas y respuestas "Ground Truth" basadas en los PDFs de prueba (ej. Guía de inmigrantes).

## Métricas a Evaluar
1. **Faithfulness (Fidelidad):** Mide si la respuesta generada se deriva *exclusivamente* del contexto recuperado. (Objetivo: > 0.90).
2. **Answer Relevance (Relevancia):** Mide si la respuesta aborda directamente la pregunta del usuario. (Objetivo: > 0.85).
3. **Context Precision (Precisión del Contexto):** Mide si los documentos recuperados son realmente útiles para responder la pregunta. (Objetivo: > 0.80).

## Implementación Técnica
El script `scripts/evaluate.py` tomará el dataset de prueba, invocará la cadena RAG y utilizará el LLM configurado como juez para calcular estas métricas. Los resultados se guardarán en un archivo CSV para su análisis.