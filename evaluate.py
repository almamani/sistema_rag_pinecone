import json

from config import BASE_DIR, RETRIEVAL_K
from documentos import cargar_documentos
from rag import RAGSystem


def calcular_metricas(
    ids_recuperados: list[str],
    ids_relevantes: list[str],
    k: int,
) -> dict[str, float]:
    if k <= 0:
        raise ValueError("k debe ser mayor que cero.")

    relevantes = set(ids_relevantes)

    if not relevantes:
        raise ValueError(
            "Cada pregunta debe tener documentos relevantes definidos."
        )

    # Eliminar repetidos conservando el orden del ranking
    recuperados = list(dict.fromkeys(ids_recuperados))[:k]

    aciertos = set(recuperados) & relevantes

    return {
        "precision": len(aciertos) / k,
        "recall": len(aciertos) / len(relevantes),
    }


def main():
    ruta = BASE_DIR / "preguntas_evaluacion.json"

    with ruta.open("r", encoding="utf-8") as archivo:
        casos = json.load(archivo)

    if not isinstance(casos, list) or len(casos) != 5:
        raise ValueError(
            "El archivo de evaluación debe contener cinco preguntas."
        )

    ids_disponibles = {
        documento.metadata["doc_id"]
        for documento in cargar_documentos()
    }

    # Revisar las referencias antes de consultar los servicios
    for caso in casos:
        if not caso["pregunta"].strip():
            raise ValueError(f"Pregunta vacía en {caso['id']}.")

        relevantes = set(caso["documentos_relevantes"])

        if not relevantes:
            raise ValueError(
                f"Faltan documentos relevantes en {caso['id']}."
            )

        desconocidos = relevantes - ids_disponibles

        if desconocidos:
            raise ValueError(
                f"Documentos inexistentes en {caso['id']}: "
                f"{sorted(desconocidos)}"
            )

    sistema = RAGSystem()

    precisiones = []
    recalls = []

    for caso in casos:
        resultados = sistema.buscar(caso["pregunta"])

        ids_recuperados = [
            documento.metadata["doc_id"]
            for documento in resultados
        ]

        ids_unicos = list(dict.fromkeys(ids_recuperados))

        metricas = calcular_metricas(
            ids_recuperados=ids_unicos,
            ids_relevantes=caso["documentos_relevantes"],
            k=RETRIEVAL_K,
        )

        precisiones.append(metricas["precision"])
        recalls.append(metricas["recall"])

        print(f"\n{caso['id']}: {caso['pregunta']}")
        print("Esperados:", caso["documentos_relevantes"])
        print("Recuperados:", ids_unicos)
        print(
            f"Precision@{RETRIEVAL_K}: "
            f"{metricas['precision']:.2%}"
        )
        print(
            f"Recall@{RETRIEVAL_K}: "
            f"{metricas['recall']:.2%}"
        )

    precision_media = sum(precisiones) / len(precisiones)
    recall_medio = sum(recalls) / len(recalls)

    print("\n=== RESUMEN DE EVALUACIÓN ===")
    print(f"Preguntas evaluadas: {len(casos)}")
    print(f"Precision@{RETRIEVAL_K} media: {precision_media:.2%}")
    print(f"Recall@{RETRIEVAL_K} medio: {recall_medio:.2%}")


if __name__ == "__main__":
    main()