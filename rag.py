import re

from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

from config import PINECONE_NAMESPACE, RETRIEVAL_K
from embeddings import obtener_embeddings
from infraestructura import preparar_indice
from documentos import cargar_documentos, fragmentar_documentos

def tokenizar_para_bm25(texto: str) -> list[str]:
    return re.findall(
        r"\b\w+(?:\.\w+)*\b",
        texto.casefold(),
    )

class RAGSystem:
    def __init__(self):
        indice = preparar_indice()
        embeddings = obtener_embeddings()

        self.vector_store = PineconeVectorStore(
            index=indice,
            embedding=embeddings,
            namespace=PINECONE_NAMESPACE,
            text_key="text",
        )

        self.recuperador_vectorial = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": RETRIEVAL_K},
        )

        documentos = cargar_documentos()
        fragmentos = fragmentar_documentos(documentos)

        self.recuperador_bm25 = BM25Retriever.from_documents(
            documents=fragmentos,
            preprocess_func=tokenizar_para_bm25,
            k=RETRIEVAL_K,
        )

        self.recuperador_hibrido = EnsembleRetriever(
            retrievers=[
                self.recuperador_bm25,
                self.recuperador_vectorial,
            ],
            weights=[0.5, 0.5],
            c=60,
            id_key="chunk_id",
        ) 

    def buscar_vectorial(self, pregunta: str) -> list[Document]:
        pregunta = pregunta.strip()

        if not pregunta:
            raise ValueError("La pregunta no puede estar vacía.")

        return self.recuperador_vectorial.invoke(pregunta)

    def buscar_bm25(self, pregunta: str) -> list[Document]:
        pregunta = pregunta.strip()

        if not pregunta:
            raise ValueError("La pregunta no puede estar vacía.")

        return self.recuperador_bm25.invoke(pregunta)

    def buscar(self, pregunta: str) -> list[Document]:
        pregunta = pregunta.strip()

        if not pregunta:
            raise ValueError("La pregunta no puede estar vacía.")

        resultados = self.recuperador_hibrido.invoke(pregunta)

        return resultados[:RETRIEVAL_K]


if __name__ == "__main__":
    sistema = RAGSystem()

    pregunta = (
        "¿Cómo puedo manejar un error durante la ejecución "
        "sin que el programa termine inmediatamente?"
    )

    resultados = sistema.buscar(pregunta)

    print(f"\nPregunta: {pregunta}")
    print(f"Resultados híbridos: {len(resultados)}")

    for posicion, documento in enumerate(resultados, start=1):
        print(
            f"{posicion}. {documento.metadata['chunk_id']} "
            f"| Fuente: {documento.metadata['source']}"
        )