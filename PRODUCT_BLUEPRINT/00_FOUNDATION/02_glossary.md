# Glosario Técnico de IA

Para entender cómo funciona este proyecto, es fundamental comprender los siguientes conceptos:

### ¿Qué es un Embedding?
Es una representación numérica (un vector) del significado semántico de un texto. Cuando enviamos un texto a un modelo de embeddings, este lo convierte en una lista de números (ej. `[0.12, -0.45, 0.88...]`). La magia es que **textos con significados similares tendrán vectores matemáticamente cercanos**.

### ¿Qué es una Base de Datos Vectorial (Vector Store)?
Es un tipo de base de datos diseñada específicamente para almacenar y buscar vectores (embeddings). A diferencia de una base de datos SQL tradicional (que busca coincidencias exactas), una base vectorial permite hacer búsquedas por **similitud semántica**. En este proyecto usamos **ChromaDB**.

### ¿Qué es RAG (Retrieval-Augmented Generation)?
Es un patrón de arquitectura que combina la búsqueda de información (Retrieval) con la generación de texto de un LLM. En lugar de preguntarle directamente al LLM (que podría alucinar), primero buscamos la respuesta en nuestros propios documentos (usando la BD Vectorial) y luego le pasamos ese contexto al LLM para que redacte una respuesta basada *estrictamente* en esa información.

### ¿Qué es un LLM (Large Language Model)?
Es el modelo de Inteligencia Artificial entrenado con grandes cantidades de texto para entender y generar lenguaje natural. En este proyecto usamos modelos de proveedores como Groq u OpenAI.

### ¿Qué es un Chunk (Fragmento)?
Como los LLMs tienen un límite de texto que pueden leer a la vez, dividimos los PDFs en trozos más pequeños (chunks) antes de convertirlos en embeddings. Esto permite que la búsqueda sea más precisa.

### ¿Qué son las Métricas de Ragas?
*   **Faithfulness (Fidelidad):** Mide si la respuesta del LLM se basa *exclusivamente* en el contexto recuperado (evita alucinaciones).
*   **Answer Relevancy (Relevancia):** Mide si la respuesta aborda directamente la pregunta del usuario.
*   **Context Precision (Precisión del Contexto):** Mide si los documentos recuperados de la base de datos vectorial son realmente útiles para responder la pregunta.
*   **Context Recall (Recuperación del Contexto):** Mide si el sistema fue capaz de recuperar toda la información necesaria que estaba en los documentos originales.

### ¿Qué es el Registry Pattern?
Es un patrón de diseño que utiliza un diccionario (o un mapa) para asociar claves (como el nombre de un proveedor de IA) con funciones constructoras. A diferencia de una cadena de `if/elif`, el Registry Pattern permite agregar nuevas funcionalidades sin modificar el código existente, cumpliendo con el principio Open/Closed de SOLID.

### ¿Qué es un Mock?
Es un objeto simulado que imita el comportamiento de un objeto real en un entorno de pruebas. Se usa para aislar el código que se está probando de dependencias externas (como APIs de terceros), permitiendo que los tests se ejecuten de forma rápida y predecible.