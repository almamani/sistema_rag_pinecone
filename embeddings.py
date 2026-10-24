from langchain_openai import OpenAIEmbeddings

from config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSION,
)


def obtener_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        api_key=OPENAI_API_KEY,
        model=EMBEDDING_MODEL,
        dimensions=EMBEDDING_DIMENSION,
    )


if __name__ == "__main__":
    embeddings = obtener_embeddings()

    texto = "Python permite manejar errores mediante excepciones."

    vector = embeddings.embed_query(texto)

    if len(vector) != EMBEDDING_DIMENSION:
        raise ValueError(
            f"Dimensión inesperada: recibimos {len(vector)} componentes."
        )

    print("Embedding generado correctamente.")
    print(f"Modelo: {EMBEDDING_MODEL}")
    print(f"Dimensión del vector: {len(vector)}")
    print(f"Primeros cinco componentes: {vector[:5]}")