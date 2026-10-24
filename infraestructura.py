import time

from pinecone import Pinecone, ServerlessSpec

from config import (
    PINECONE_API_KEY,
    INDEX_NAME,
    EMBEDDING_DIMENSION,
    PINECONE_CLOUD,
    PINECONE_REGION,
)


def preparar_indice():
    pc = Pinecone(api_key=PINECONE_API_KEY)

    if INDEX_NAME not in pc.list_indexes().names():
        print(f"Creando el índice '{INDEX_NAME}'...")

        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=PINECONE_CLOUD,
                region=PINECONE_REGION,
            ),
            timeout=-1,
        )
    else:
        print(f"El índice '{INDEX_NAME}' ya existe.")

    limite_espera = time.monotonic() + 120

    while True:
        descripcion = pc.describe_index(INDEX_NAME)

        if descripcion.status["ready"]:
            break

        if time.monotonic() >= limite_espera:
            raise TimeoutError(
                "El índice no estuvo listo dentro del tiempo de espera."
            )

        print("Esperando a que el índice esté listo...")
        time.sleep(2)

    if descripcion.dimension != EMBEDDING_DIMENSION:
        raise ValueError(
            f"Dimensión incompatible: el índice tiene "
            f"{descripcion.dimension} y esperamos {EMBEDDING_DIMENSION}."
        )

    if descripcion.metric != "cosine":
        raise ValueError(
            f"Métrica incompatible: el índice utiliza "
            f"'{descripcion.metric}' y esperamos 'cosine'."
        )

    index = pc.Index(host=descripcion.host)

    print(f"Índice '{INDEX_NAME}' listo.")
    print(f"Dimensión: {descripcion.dimension}")
    print(f"Métrica: {descripcion.metric}")

    return index


if __name__ == "__main__":
    indice = preparar_indice()

    print("Estadísticas:")
    print(indice.describe_index_stats())

