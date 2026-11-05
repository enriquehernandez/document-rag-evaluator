from app.core.embeddings_factory import get_embeddings
from app.core.config import settings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import sys
import hashlib
import shutil
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).resolve().parent.parent))


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "chroma_db"


def _get_pdf_files() -> List[Path]:
    """Obtiene la lista de archivos PDF validando que existan."""
    pdf_files = list(DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ No se encontraron archivos PDF en {DATA_DIR}")
        return []
    print(f"📄 Se encontraron {len(pdf_files)} archivos PDF.")
    return pdf_files


def _process_full_ingest(pdf_files: List[Path], embeddings):
    """Limpia la base de datos y procesa todos los PDFs desde cero."""
    if DB_DIR.exists():
        print("🧹 [MODO FULL] Limpiando base de datos vectorial anterior...")
        shutil.rmtree(DB_DIR)

    all_splits = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        # <-- Prioriza cortar por párrafos y oraciones
        separators=["\n\n", "\n", ".", " ", ""]
    )

    for pdf_path in pdf_files:
        print(f"⏳ Procesando completo: {pdf_path.name}...")
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        splits = text_splitter.split_documents(docs)

        # ✨ AGREGAMOS LA LÓGICA DEL HASH AQUÍ TAMBIÉN
        file_hash = _generate_file_hash(pdf_path)
        for split in splits:
            split.metadata["file_hash"] = file_hash

        all_splits.extend(splits)

    print(f"✂️ Se dividieron los documentos en {len(all_splits)} chunks.")
    print("💾 Guardando en ChromaDB...")
    Chroma.from_documents(documents=all_splits,
                          embedding=embeddings, persist_directory=str(DB_DIR))
    print("✅ ¡Ingesta FULL completada!")


def _generate_file_hash(pdf_path: Path) -> str:
    """Genera un hash MD5 rápido basado en el nombre y peso del archivo."""
    file_stats = pdf_path.stat()
    file_signature = f"{pdf_path.name}_{file_stats.st_size}"
    return hashlib.md5(file_signature.encode()).hexdigest()


def _process_incremental_ingest(pdf_files: List[Path], embeddings):
    """Procesa solo los PDFs que no existan previamente en la base de datos."""
    print("🔍 [MODO INCREMENTAL] Verificando documentos nuevos...")

    # Nos conectamos a la base de datos
    vectorstore = Chroma(persist_directory=str(
        DB_DIR), embedding_function=embeddings)

    # ✨ EL TRUCO: Obtenemos TODOS los hashes que ya están en la BD
    # Buscamos solo los metadatos (que es más rápido que traer los vectores)
    existing_data = vectorstore.get(include=["metadatas"])

    # Creamos un set (conjunto) con los hashes ya guardados para búsquedas ultrarrápidas
    existing_hashes = set()
    if existing_data and existing_data.get('metadatas'):
        for meta in existing_data['metadatas']:
            if meta and 'file_hash' in meta:
                existing_hashes.add(meta['file_hash'])

    print(
        f"📊 La base de datos actualmente tiene {len(existing_hashes)} archivos indexados.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        # <-- Prioriza cortar por párrafos y oraciones
        separators=["\n\n", "\n", ".", " ", ""]
    )
    new_splits = []

    for pdf_path in pdf_files:
        file_hash = _generate_file_hash(pdf_path)

        # ✨ Comparamos el hash del PDF actual con los hashes que ya tenemos
        if file_hash in existing_hashes:
            print(f"⏭️ Saltando {pdf_path.name} (ya está procesado).")
            continue

        print(f"⏳ Procesando nuevo: {pdf_path.name}...")
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        splits = text_splitter.split_documents(docs)

        for split in splits:
            split.metadata["file_hash"] = file_hash
        new_splits.extend(splits)

    if not new_splits:
        print("✅ No hay documentos nuevos. La base de datos está actualizada.")
        return

    print(f"✂️ Se procesarán {len(new_splits)} chunks nuevos.")
    print("💾 Agregando a ChromaDB...")
    vectorstore.add_documents(new_splits)
    print("✅ ¡Ingesta INCREMENTAL completada!")


def ingest_documents():
    """Punto de entrada principal que delega la lógica según el modo."""
    mode = settings.INGEST_MODE.upper()
    print(f"🚀 Iniciando proceso de ingesta en modo: {mode}")

    pdf_files = _get_pdf_files()
    if not pdf_files:
        return  # Salida temprana si no hay archivos

    embeddings = get_embeddings()

    if mode == "FULL":
        _process_full_ingest(pdf_files, embeddings)
    elif mode == "INCREMENTAL":
        _process_incremental_ingest(pdf_files, embeddings)
    else:
        print(f"❌ Modo de ingesta '{mode}' no válido. Usa FULL o INCREMENTAL.")


if __name__ == "__main__":
    ingest_documents()
