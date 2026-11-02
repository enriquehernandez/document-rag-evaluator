from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.rag_engine import RAGEngine
from app.core.config import settings

app = FastAPI(
    title="Advanced RAG Evaluator API",
    description="API para consultar documentos PDF usando LLMs.",
    version="1.0.0"
)

# Instanciamos el motor RAG
rag_engine = RAGEngine()


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "llm_provider": settings.LLM_PROVIDER,
        "embedding_provider": settings.EMBEDDING_PROVIDER
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_with_docs(request: ChatRequest):
    try:
        chain = rag_engine.get_chain()
        # Invocamos la cadena con la pregunta del usuario
        response = chain.invoke(request.query)
        return ChatResponse(answer=response)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, detail="Error interno procesando la solicitud")
