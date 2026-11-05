from app.core.config import settings
from app.services.rag_engine import RAGEngine
import asyncio
import sys
import os
import pandas as pd
from pathlib import Path
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
# ✨ CONFIGURACIÓN CLAVE: Decirle a Ragas que use Groq/OpenRouter en vez de OpenAI
from app.core.llm_factory import get_llm
from app.core.embeddings_factory import get_embeddings

# Asegurar que Python encuentre la carpeta 'app'
sys.path.append(str(Path(__file__).resolve().parent.parent))


# 1. Definir el Dataset de Evaluación (Ground Truth)
# Estas preguntas deben basarse en los PDFs que subiste a la carpeta /data
eval_dataset = [
    # ==========================================
    # PREGUNTAS DEL PDF: Guía para nuevos inmigrantes
    # ==========================================
    {
        "question": "¿Cuál es el número de teléfono del Servicio de Ciudadanía e Inmigración de Estados Unidos (USCIS) para personas con discapacidades auditivas?",
        "ground_truth": "El número es 1-800-767-1833."
    },
    {
        "question": "Si un residente permanente se muda de casa, ¿dentro de cuántos días debe notificar su nueva dirección a USCIS?",
        "ground_truth": "Debe notificarlo dentro de los 10 días posteriores a la mudanza presentando el Formulario AR-11."
    },
    {
        "question": "¿Cuáles son los dos tipos de cuentas bancarias más comunes que menciona la guía?",
        "ground_truth": "Las cuentas corrientes y las cuentas de ahorro."
    },
    {
        "question": "¿Qué debes hacer si un oficial de policía te detiene mientras conduces y no hablas inglés?",
        "ground_truth": "Debes decirle al oficial de policía que no hablas inglés, ser cortés, cooperar, no salir del automóvil antes de que el policía te lo indique y mantener las manos donde el oficial las pueda ver."
    },
    {
        "question": "¿Cuál es el requisito de presencia física en Estados Unidos para solicitar la naturalización si estás casado con un ciudadano estadounidense?",
        "ground_truth": "Debes haber estado físicamente en Estados Unidos durante 18 meses como mínimo durante los últimos tres años antes de solicitar la naturalización."
    },

    # ==========================================
    # PREGUNTAS DEL PDF: International Express
    # ==========================================
    {
        "question": "¿Cuándo se firmó la Declaración de Independencia de Estados Unidos y qué día celebran los estadounidenses?",
        "ground_truth": "Se firmó el 4 de julio de 1776. Los estadounidenses celebran el Día de la Independencia el 4 de julio."
    },
    {
        "question": "¿Cuáles son las dos cosas que hacen a los humanos diferentes de los animales, según el texto sobre la gramática de la ropa?",
        "ground_truth": "Hablamos lenguajes y usamos ropa."
    },
    {
        "question": "En la entrevista sobre la diseñadora Zaha Hadid, ¿de dónde viene la idea para su diseño de sofás llamado 'Dune Formations'?",
        "ground_truth": "La idea proviene de los desiertos sumerios que visitó cuando era adolescente."
    },
    {
        "question": "¿Qué pasa en el juego de construcción de equipos (team-building) llamado 'The tyre game'?",
        "ground_truth": "Los equipos forman un círculo, se dan la mano y deben pasarse un neumático de bicicleta por el cuerpo hasta que vuelva a su posición original, sin soltarse de las manos."
    }
]


async def run_evaluation():
    print(
        f"🚀 Iniciando evaluación con Ragas usando {settings.LLM_PROVIDER}...")

    # Inicializar el motor RAG
    rag_engine = RAGEngine()

    questions = []
    answers = []
    contexts = []
    ground_truths = []

    # 2. Generar respuestas usando nuestro RAG
    for item in eval_dataset:
        print(f"⏳ Evaluando pregunta: {item['question']}")

        # Obtener la respuesta del RAG
        result = await rag_engine.get_answer_with_sources(item["question"])

        questions.append(item["question"])
        answers.append(result["answer"])
        ground_truths.append(item["ground_truth"])

        # Ragas necesita el contexto (los documentos recuperados) como una lista de strings
        # En nuestro RAGEngine actual, no estamos devolviendo el texto de los documentos,
        # así que haremos una búsqueda rápida aquí para obtenerlos.
        docs = rag_engine.retriever.invoke(item["question"])
        contexts.append([doc.page_content for doc in docs])

    # 3. Crear el Dataset para Ragas
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    dataset = Dataset.from_dict(data)

    # 4. Ejecutar la evaluación
    ragas_llm = LangchainLLMWrapper(get_llm())
    ragas_embeddings = LangchainEmbeddingsWrapper(get_embeddings())
    print("🧠 Calculando métricas con Ragas (esto puede tardar unos minutos)...")

    # ✨ SOLUCIÓN: Forzar a que AnswerRelevancy use n=1 (strictness)
    # Esto evita que Ragas intente pedir 3 respuestas a Groq
    answer_relevancy.strictness = 1

    result = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall
        ],
        llm=ragas_llm,              # <-- Le pasamos el LLM de Groq
        embeddings=ragas_embeddings,  # <-- Le pasamos los embeddings de OpenRouter
        # <-- Si una métrica falla para una fila, no lances una excepción que detenga todo el proceso; simplemente devuelve NaN (Not a Number) para esa fil
        raise_exceptions=False
    )

    # 5. Guardar y mostrar resultados
    print("\n✅ Evaluación completada. Resultados:")
    print(result)

    df = result.to_pandas()

    output_path = Path(__file__).resolve().parent.parent / \
        "evaluation_results.csv"
    df.to_csv(output_path, index=False)
    print(f"\n📊 Resultados detallados guardados en: {output_path}")


if __name__ == "__main__":
    asyncio.run(run_evaluation())
