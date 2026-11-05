# Security Policy

En sistemas basados en IA, la seguridad es crítica. Este proyecto implementa las siguientes medidas:

## 1. Manejo de Secretos (API Keys)
- **Cero Hardcoding:** Ninguna API Key está escrita en el código fuente.
- **Variables de Entorno:** Se utiliza un archivo `.env` (local) que está estrictamente excluido del control de versiones en `.gitignore`.
- **Plantilla:** El archivo `.env.example` provee la estructura pero no los valores reales.

## 2. Protección contra Prompt Injection
- El Prompt del sistema (System Prompt) instruye estrictamente al LLM a responder **solo** basándose en el contexto proporcionado.
- Si un usuario intenta inyectar código malicioso en el chat para alterar las reglas del sistema, el orquestador de LangChain limitará la respuesta al contexto recuperado.

## 3. Privacidad de los Datos (Data Privacy)
- Los PDFs utilizados en la ingesta son eliminados de la base de datos vectorial si se vuelve a correr el script (`shutil.rmtree`).
- Las búsquedas vectoriales se realizan localmente (ChromaDB). Solo el texto de los *chunks* recuperados viaja al proveedor del LLM (Groq/OpenAI).