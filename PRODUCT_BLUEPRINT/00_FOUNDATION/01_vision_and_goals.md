# Vision and Goals

## Visión
Crear una API REST de nivel producción que sirva como motor de búsqueda inteligente para cualquier empresa que necesite consultar su documentación interna de forma segura y precisa.

## Objetivos Técnicos (Goals)
1. **Precisión (Accuracy):** Minimizar las alucinaciones del LLM mediante la inyección estricta de contexto.
2. **Flexibilidad (Provider-Agnostic):** Desacoplar la lógica de negocio del proveedor de IA (Patrón Factory).
3. **Rendimiento:** Utilizar búsqueda híbrida (Vectorial + BM25) para recuperar los fragmentos más relevantes.
4. **Calidad Medible:** Implementar un pipeline de evaluación con *Ragas* para auditar la calidad del sistema antes de cada despliegue.