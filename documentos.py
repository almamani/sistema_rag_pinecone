from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    BASE_DIR,
    CHUNK_SIZE_TOKENS,
    CHUNK_OVERLAP_TOKENS,
)


DOCS_DIR = BASE_DIR / "docs"


def cargar_documentos() -> list[Document]:
    if not DOCS_DIR.is_dir():
        raise FileNotFoundError(
            f"No existe la carpeta de documentos: {DOCS_DIR}"
        )

    archivos = sorted(DOCS_DIR.glob("*.md"))

    if not archivos:
        raise ValueError("No se encontraron archivos Markdown en docs.")

    documentos = []

    for archivo in archivos:
        texto = archivo.read_text(encoding="utf-8").strip()

        if not texto:
            raise ValueError(f"El archivo está vacío: {archivo.name}")

        fuente_url = next(
            (
                linea.removeprefix("Fuente: ").strip()
                for linea in texto.splitlines()
                if linea.startswith("Fuente: ")
            ),
            "",
        )

        if not fuente_url:
            raise ValueError(
                f"Falta la fuente oficial en: {archivo.name}"
            )

        documento = Document(
            page_content=texto,
            metadata={
                "doc_id": archivo.stem,
                "source": archivo.name,
                "source_url": fuente_url,
                "category": "python",
                "format": "markdown",
            },
        )

        documentos.append(documento)

    return documentos

def fragmentar_documentos(
    documentos: list[Document],
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=CHUNK_SIZE_TOKENS,
        chunk_overlap=CHUNK_OVERLAP_TOKENS,
    )

    fragmentos = []

    for documento in documentos:
        partes = splitter.split_documents([documento])

        for numero, fragmento in enumerate(partes, start=1):
            doc_id = documento.metadata["doc_id"]

            fragmento.metadata["chunk_index"] = numero
            fragmento.metadata["chunk_id"] = (
                f"{doc_id}::chunk-{numero}"
            )

            fragmentos.append(fragmento)

    return fragmentos


if __name__ == "__main__":
    documentos = cargar_documentos()
    fragmentos = fragmentar_documentos(documentos)

    print(f"Documentos cargados: {len(documentos)}")
    print(f"Fragmentos generados: {len(fragmentos)}")

    for fragmento in fragmentos:
        print(
            f"- {fragmento.metadata['chunk_id']} "
            f"| Caracteres: {len(fragmento.page_content)}"
        )

    print("\nMetadatos del primer fragmento:")
    print(fragmentos[0].metadata)