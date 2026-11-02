from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from app.core.llm_factory import get_llm
from app.core.embeddings_factory import get_embeddings
from pathlib import Path

# Ruta de la base de datos
DB_DIR = Path(__file__).resolve().parent.parent.parent / "chroma_db"


class RAGEngine:
    def __init__(self):
        self.llm = get_llm()

        # Cargamos la base de datos que creamos con ingest.py
        self.embeddings = get_embeddings()
        self.vectorstore = Chroma(
            persist_directory=str(DB_DIR),
            embedding_function=self.embeddings
        )

        # Buscaremos los 4 fragmentos más relevantes
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})

        # El prompt del sistema (Optimizado para RAG)
        system_prompt = (
            "Eres un asistente experto. Utiliza los siguientes fragmentos de contexto "
            "para responder la pregunta del usuario. Si no sabes la respuesta, di "
            "claramente que no tienes información suficiente en los documentos proporcionados. "
            "Siempre intenta citar de qué documento proviene la información.\n\n"
            "Contexto:\n{context}"
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

    def _format_docs(self, docs):
        # Une los fragmentos recuperados en un solo texto
        return "\n\n".join(doc.page_content for doc in docs)

    def get_chain(self):
        # Cadena LCEL moderna
        return (
            {"context": self.retriever | self._format_docs,
                "input": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
