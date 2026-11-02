from typing import List

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


class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []
    tokens_used: TokenUsage


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
        # Obtenemos la respuesta y los documentos fuente
        result = await rag_engine.get_answer_with_sources(request.query)
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            tokens_used=result["tokens_used"]
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, detail="Error interno procesando la solicitud")
