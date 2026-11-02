# Evaluation Plan & Results (Ragas)

Para asegurar que el sistema está listo para producción, implementamos un pipeline de evaluación automatizado utilizando la librería **Ragas**. El script `scripts/evaluate.py` toma un set de preguntas "Ground Truth" basadas en los PDFs cargados y calcula métricas de calidad usando el LLM configurado como juez.

## 📊 Resultados de la Última Evaluación

A continuación se presentan los resultados obtenidos utilizando **Groq (`openai/gpt-oss-120b`)** como LLM evaluador:

| Métrica | Puntaje | Objetivo | Estado | Análisis |
| :--- | :--- | :--- | :--- | :--- |
| **Context Recall** | `1.0000` | > 0.80 | ✅ Excelente | El 100% de los fragmentos necesarios fueron recuperados por ChromaDB. |
| **Answer Relevancy** | `0.7114` | > 0.85 | ⚠️ Aceptable | El LLM responde a la pregunta, pero puede mejorar en concisión. |
| **Context Precision** | `0.6500` | > 0.80 | ⚠️ Aceptable | Algunos fragmentos recuperados no eran útiles (se puede ajustar el `k` o usar MMR). |
| **Faithfulness** | `NaN` | > 0.90 | ❌ Fallido | Error de API: Groq no soporta `n>1` (múltiples generaciones) requerido por Ragas. |

*(Nota: El error de `Faithfulness` se debió a limitaciones de la API de Groq al no permitir `n=3`. Se solucionará forzando `n=1` en el cliente o usando OpenRouter como juez).*

## 🛠️ Plan de Mejoras (Action Items)
1.  **Solucionar Faithfulness:** Modificar el `LangchainLLMWrapper` para forzar `n=1` y aumentar el `max_tokens`.
2.  **Mejorar Context Precision:** Implementar búsqueda MMR (Maximum Marginal Relevance) en el retriever para evitar fragmentos redundantes.
3.  **Ajustar Prompt:** Refinar el System Prompt para que las respuestas sean más directas y aumenten el `Answer Relevancy`.