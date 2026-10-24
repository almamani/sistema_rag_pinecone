from datetime import datetime, UTC

from config import PINECONE_NAMESPACE, EMBEDDING_DIMENSION
from documentos import cargar_documentos, fragmentar_documentos
from embeddings import obtener_embeddings
from infraestructura import preparar_indice


def ejecutar_ingesta(batch_size: int = 2) -> int:
    if batch_size <= 0:
        raise ValueError("El tamaño de lote debe ser mayor que cero.")

    documentos = cargar_documentos()
    fragmentos = fragmentar_documentos(documentos)

    indice = preparar_indice()
    embeddings = obtener_embeddings()

    total_cargado = 0

    for inicio in range(0, len(fragmentos), batch_size):
        lote = fragmentos[inicio:inicio + batch_size]

        textos = [
            fragmento.page_content
            for fragmento in lote
        ]

        vectores = embeddings.embed_documents(textos)

        registros = []

        for fragmento, vector in zip(lote, vectores, strict=True):
            if len(vector) != EMBEDDING_DIMENSION:
                raise ValueError(
                    f"Dimensión incorrecta en "
                    f"{fragmento.metadata['chunk_id']}: {len(vector)}"
                )

            metadata = {
                **fragmento.metadata,
                "text": fragmento.page_content,
                "ingested_at": datetime.now(UTC).isoformat(),
            }

            registros.append({
                "id": fragmento.metadata["chunk_id"],
                "values": vector,
                "metadata": metadata,
            })

        resultado = indice.upsert(
            vectors=registros,
            namespace=PINECONE_NAMESPACE,
        )

        total_cargado += resultado.upserted_count

        print(
            f"Lote {inicio // batch_size + 1}: "
            f"{resultado.upserted_count} registros cargados."
        )

    return total_cargado


if __name__ == "__main__":
    total = ejecutar_ingesta()

    print(f"\nIngesta finalizada. Total cargado: {total}")
    print(f"Namespace: {PINECONE_NAMESPACE}")