# Entendiendo la Métrica de Faithfulness (Fidelidad)

En nuestro pipeline de evaluación automatizada con **Ragas**, la métrica de **Faithfulness** (Fidelidad) es la más crítica. Este documento explica qué es, por qué es vital para nuestro sistema RAG y cómo Ragas la calcula internamente.

## ¿Qué es el Faithfulness?
El **Faithfulness** mide si la respuesta generada por el LLM se deriva **exclusivamente** del contexto recuperado de nuestra base de datos vectorial (ChromaDB). 
*   **Puntaje de 1.0:** La respuesta está 100% respaldada por los documentos. No hay alucinaciones.
*   **Puntaje de 0.0:** El LLM ignoró el contexto e inventó la información (alucinación total).

En un sistema RAG, el objetivo principal es eliminar las alucinaciones. Por lo tanto, el Faithfulness es el indicador definitivo de que nuestro sistema está funcionando como debería.

## ¿Cómo lo calcula Ragas internamente? (El proceso de 3 pasos)
Como desarrolladores, no calculamos esto matemáticamente con fórmulas complejas. Ragas utiliza un "LLM Juez" (en nuestro caso, Groq) para hacer el trabajo pesado. El proceso es el siguiente:

1.  **Descomposición (Descompose):** El LLM Juez analiza la respuesta generada y la divide en "afirmaciones" o hechos independientes (claims). 
    *   *Ejemplo:* Si la respuesta es *"El límite de velocidad es 60 km/h y el conductor debe usar cinturón"*, Ragas lo divide en:
        *   Claim 1: El límite de velocidad es 60 km/h.
        *   Claim 2: El conductor debe usar cinturón.
2.  **Verificación (Verification):** El LLM Juez revisa *cada una* de esas afirmaciones contra el contexto original recuperado de ChromaDB. Se pregunta a sí mismo: *"¿Esta afirmación se puede deducir directamente del texto recuperado?"*.
3.  **Cálculo (Scoring):** Se calcula la proporción de afirmaciones que fueron respaldadas por el contexto frente al total de afirmaciones.
    *   *Fórmula:* `Faithfulness = (Afirmaciones respaldadas) / (Total de afirmaciones)`.

## ¿Dónde se ve esto en el código?
El cálculo no vive en nuestra API (`app/`). La API solo se encarga de generar respuestas. El Faithfulness es una tarea de auditoría que se ejecuta en el script **`scripts/evaluate.py`**.

1.  Se importa la métrica:
    ```python
    from ragas.metrics.collections import faithfulness