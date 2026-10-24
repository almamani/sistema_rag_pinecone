import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


def obtener_variable_requerida(nombre: str) -> str:
    valor = os.getenv(nombre, "").strip()

    if not valor:
        raise ValueError(
            f"Falta configurar la variable de entorno: {nombre}"
        )

    return valor


PINECONE_API_KEY = obtener_variable_requerida("PINECONE_API_KEY")
OPENAI_API_KEY = obtener_variable_requerida("OPENAI_API_KEY")
INDEX_NAME = obtener_variable_requerida("INDEX_NAME")
PINECONE_NAMESPACE = obtener_variable_requerida("PINECONE_NAMESPACE")

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536

PINECONE_CLOUD = "aws"
PINECONE_REGION = "us-east-1"

CHUNK_SIZE_TOKENS = 600
CHUNK_OVERLAP_TOKENS = 80

RETRIEVAL_K = 5


if __name__ == "__main__":
    print("Configuración cargada correctamente.")
    print(f"Índice: {INDEX_NAME}")
    print(f"Namespace: {PINECONE_NAMESPACE}")
    print(f"Modelo de embeddings: {EMBEDDING_MODEL}")
    print(f"Dimensión: {EMBEDDING_DIMENSION}")