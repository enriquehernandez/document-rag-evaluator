# Problem Statement

## Contexto
En industrias como la banca, seguros o el sector público, los analistas pierden horas revisando manuales de procedimientos, contratos o documentación técnica en formato PDF. Aunque los LLMs (como ChatGPT) pueden responder preguntas, sufren de dos problemas críticos:
1. **Alucinaciones:** Inventan información si no conocen la respuesta.
2. **Falta de contexto empresarial:** No tienen acceso a la documentación privada de la organización.

## Solución Propuesta
Desarrollar un sistema RAG (Retrieval-Augmented Generation) que:
- Permita a los usuarios hacer preguntas en lenguaje natural sobre documentos internos.
- Base sus respuestas **únicamente** en los documentos proporcionados (citando la fuente).
- Incluya un **sistema de evaluación automática** que mida matemáticamente la calidad de las respuestas para evitar alucinaciones.
- Sea agnóstico al proveedor de IA (permite cambiar entre OpenAI, Groq, Claude, etc., mediante configuración).