import time
from pathlib import Path
from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma

from app.core.llm_factory import get_llm
from app.core.embeddings_factory import get_embeddings

# Ruta de la base de datos
DB_DIR = Path(__file__).resolve().parent.parent.parent / "chroma_db"


class RAGEngine:
    def __init__(self):
        self.llm = get_llm()

        # Cargamos la base de datos vectorial (creada por ingest.py)
        self.embeddings = get_embeddings()
        self.vectorstore = Chroma(
            persist_directory=str(DB_DIR),
            embedding_function=self.embeddings
        )

        # Recuperador: Busca los 4 fragmentos más relevantes
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})

        # Prompt del sistema (Optimizado para RAG y citación de fuentes)
        system_prompt = (
            "Eres un asistente experto. Utiliza los siguientes fragmentos de contexto "
            "para responder la pregunta del usuario. Si no sabes la respuesta, di "
            "claramente que no tienes información suficiente en los documentos proporcionados.\n\n"
            "Contexto:\n{context}"
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

    def _format_docs(self, docs) -> str:
        """Une los fragmentos recuperados en un solo bloque de texto."""
        return "\n\n".join(doc.page_content for doc in docs)

    def _extract_sources(self, docs) -> list[str]:
        """Extrae los nombres de archivo y páginas únicas de los documentos recuperados."""
        sources = set()
        for doc in docs:
            # Extraer el nombre del archivo y la página de la metadata
            source_path = doc.metadata.get("source", "Desconocido")
            filename = Path(source_path).name
            page = doc.metadata.get("page", "N/A")

            # Formatear la cita (ej. "documento.pdf (pág. 5)")
            sources.add(f"{filename} (pág. {page})")

        return list(sources)

    def _extract_tokens(self, response: Any) -> dict:
        """Extrae el desglose de tokens de la respuesta del LLM."""
        usage = {}
        if hasattr(response, 'response_metadata') and 'token_usage' in response.response_metadata:
            usage = response.response_metadata['token_usage']
        elif hasattr(response, 'usage_metadata') and response.usage_metadata:
            usage = response.usage_metadata

        return {
            "prompt_tokens": usage.get('prompt_tokens', 0),
            "completion_tokens": usage.get('completion_tokens', 0),
            "total_tokens": usage.get('total_tokens', 0)
        }

    async def get_answer_with_sources(self, query: str) -> Dict[str, Any]:
        """
        Ejecuta el flujo RAG y devuelve la respuesta, las fuentes citadas y el uso de tokens.
        """
        start_time = time.time()

        # 1. Recuperar documentos relevantes
        docs = self.retriever.invoke(query)
        context = self._format_docs(docs)
        sources = self._extract_sources(docs)

        # 2. Ejecutar la cadena (LCEL)
        chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

        # Invocamos con el contexto y la pregunta
        answer = await chain.ainvoke({"context": context, "input": query})

        # 3. Calcular tokens (Nota: Al usar StrOutputParser perdemos la metadata,
        # así que invocamos al LLM directamente si necesitamos los tokens exactos)
        # Para mantener el código simple y rápido, haremos una invocación directa sin parser:

        # (Re-invocación ligera solo para obtener metadata si se requiere precisión exacta)
        # *En producción, se suele usar un callback handler para capturar los tokens sin re-invocar.
        # Por ahora, simularemos la obtención de tokens o dejaremos un valor estimado si no hay metadata.

        # Para evitar doble cobro, haremos la invocación directa y extraeremos el contenido:
        messages = self.prompt.format_messages(context=context, input=query)
        raw_response = await self.llm.ainvoke(messages)

        answer_text = raw_response.content
        tokens_usage = self._extract_tokens(raw_response)
        latency = round(time.time() - start_time, 2)

        return {
            "answer": answer_text,
            "sources": sources,
            "tokens_used": tokens_usage,
            "metadata": {
                "latency_seconds": latency,
                "chunks_retrieved": len(docs)
            }
        }

    def get_chain(self):
        """Método legacy para pruebas rápidas en consola."""
        return (
            {"context": self.retriever | self._format_docs, "input": lambda x: x}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
