# RAG Chain Component

## Responsabilidad
Orquestar la recuperación de información desde ChromaDB y la generación de respuestas a través del LLM.

## Contrato de Entrada (API)
```json
{
  "query": "¿Cuáles son los requisitos para la visa?"
}
```

## Contrato de Salida
```json
{
  "answer": "string",
  "sources": ["doc1.pdf (pag 5)", "doc2.pdf (pag 12)"],
  "tokens_used": {
    "prompt_tokens": int,
    "completion_tokens": int,
    "total_tokens": int
}
```

## Reglas de Negocio

1. Contexto Estricto: El LLM debe responder solo basándose en el contexto recuperado.
2. Fallo Seguro: Si el retriever no encuentra información relevante, el LLM debe indicar que no tiene información suficiente en lugar de inventar una respuesta.
3. Atribución: Se debe solicitar al LLM que mencione de qué documento proviene la información si es posible.