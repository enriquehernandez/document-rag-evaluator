from app.core.embeddings_factory import get_embeddings
from app.core.config import settings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import shutil
import sys
from pathlib import Path

# Asegurar que Python encuentre la carpeta raíz 'app'
sys.path.append(str(Path(__file__).resolve().parent.parent))


# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "chroma_db"


def ingest_documents():
    print("🚀 Iniciando proceso de ingesta de documentos...")

    # 1. Validar que existan archivos PDF en la carpeta data
    pdf_files = list(DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No se encontraron archivos PDF en {DATA_DIR}")
        print("Por favor, coloca algunos PDFs en la carpeta 'data' y vuelve a intentar.")
        return

    print(f"📄 Se encontraron {len(pdf_files)} archivos PDF.")

    # 2. Limpiar la base de datos vectorial anterior (evita duplicados)
    if DB_DIR.exists():
        print("🧹 Limpiando base de datos vectorial anterior...")
        shutil.rmtree(DB_DIR)

    # 3. Cargar y dividir los documentos
    all_splits = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    for pdf_path in pdf_files:
        print(f"⏳ Procesando: {pdf_path.name}...")
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()

        splits = text_splitter.split_documents(docs)
        all_splits.extend(splits)

    print(
        f"✂️ Se dividieron los documentos en {len(all_splits)} chunks (fragmentos).")

    # 4. Crear Embeddings usando la fábrica (OpenRouter/OpenAI/HuggingFace)
    print(
        f"🧠 Generando embeddings usando el proveedor: {settings.EMBEDDING_PROVIDER}...")
    embeddings = get_embeddings()

    # 5. Guardar en la base de datos vectorial ChromaDB
    print("💾 Guardando en ChromaDB (esto puede tardar un poco)...")
    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=embeddings,
        persist_directory=str(DB_DIR)
    )

    print(
        f"✅ ¡Ingesta completada con éxito! Base de datos guardada en: {DB_DIR}")


if __name__ == "__main__":
    ingest_documents()
