# Sistema de recuperación híbrida con Pinecone

Preentrega 4 del curso AI Engineering. Recupera documentación técnica de Python mediante búsqueda vectorial en Pinecone Serverless y búsqueda léxica BM25, combinadas con Reciprocal Rank Fusion (RRF).

El sistema devuelve los cinco fragmentos mejor posicionados. Su alcance es la recuperación documental y su evaluación; no genera respuestas conversacionales con un LLM.

## Tecnologías

- Python 3.12.
- Pinecone Serverless, AWS `us-east-1`, métrica coseno.
- Embeddings OpenAI `text-embedding-3-small`, con 1536 dimensiones.
- LangChain: `PineconeVectorStore`, `BM25Retriever`, `EnsembleRetriever` y `RecursiveCharacterTextSplitter`.
- `unittest` para comprobar las métricas.

## Estructura

| Archivo o carpeta | Responsabilidad |
|---|---|
| `config.py` | Carga y valida variables de entorno; centraliza constantes. |
| `infraestructura.py` | Crea el índice si falta, espera su disponibilidad y verifica dimensión y métrica. |
| `embeddings.py` | Configura el cliente de embeddings y permite probarlo. |
| `docs/` | Ocho documentos Markdown sobre Python 3.12. |
| `documentos.py` | Lee los documentos, conserva sus fuentes y genera fragmentos identificados. |
| `ingesta.py` | Genera embeddings y carga registros por lotes. |
| `rag.py` | Implementa `RAGSystem`, los recuperadores individuales y la búsqueda híbrida. |
| `preguntas_evaluacion.json` | Cinco preguntas con fuentes relevantes y respuestas de referencia. |
| `evaluate.py` | Calcula Precision@5 y Recall@5 por pregunta y sus promedios. |
| `test_evaluate.py` | Pruebas unitarias de métricas y entradas inválidas. |
| `.env.example` | Plantilla de configuración sin credenciales. |
| `requirements.txt` | Versiones de las dependencias del entorno. |

## Preparación

Se necesitan Python 3.12, acceso a un proyecto de Pinecone y una API key de OpenAI con acceso a embeddings. La ingesta y la búsqueda vectorial realizan llamadas a servicios externos y pueden generar cargos según el uso y el plan de cada servicio.

Los comandos siguientes se ejecutan desde la raíz del repositorio en PowerShell. Usan directamente el Python del entorno, por lo que no requieren activar scripts.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
Copy-Item .env.example .env
```

Editar `.env` con las claves reales:

```dotenv
PINECONE_API_KEY=tu_clave_de_pinecone
OPENAI_API_KEY=tu_clave_de_openai
INDEX_NAME=preentrega4-rag
PINECONE_NAMESPACE=documentacion-tecnica
```

El archivo `.env` está excluido mediante `.gitignore`. Mantener vacías las claves de `.env.example` en el repositorio.

Comprobar la carga de configuración:

```powershell
.\.venv\Scripts\python.exe config.py
```

Salida esperada:

```text
Configuración cargada correctamente.
Índice: preentrega4-rag
Namespace: documentacion-tecnica
Modelo de embeddings: text-embedding-3-small
Dimensión: 1536
```

Esta comprobación valida la presencia de los valores; su autenticación se comprueba al consultar cada servicio.

## Crear el índice e ingerir documentos

```powershell
.\.venv\Scripts\python.exe infraestructura.py
.\.venv\Scripts\python.exe documentos.py
.\.venv\Scripts\python.exe ingesta.py
```

La infraestructura crea `preentrega4-rag` si no existe y comprueba que acepte vectores de 1536 dimensiones con métrica coseno. El namespace se crea con la primera carga.

La fragmentación utiliza un máximo de 600 tokens, medidos con `cl100k_base`, y un solapamiento configurado de hasta 80 tokens. Los ocho documentos actuales caben individualmente dentro del máximo y producen ocho fragmentos.

Cada registro guarda su vector y los metadatos `doc_id`, `source`, `source_url`, `category`, `format`, `chunk_index`, `chunk_id`, `text` e `ingested_at`. El texto original del fragmento se conserva en `text`. Los Markdown no tienen paginación: su localización se identifica mediante archivo, URL e índice de fragmento.

La ingesta predeterminada procesa lotes de dos. Salida esperada, además de los mensajes de infraestructura:

```text
Lote 1: 2 registros cargados.
Lote 2: 2 registros cargados.
Lote 3: 2 registros cargados.
Lote 4: 2 registros cargados.

Ingesta finalizada. Total cargado: 8
Namespace: documentacion-tecnica
```

Para consultar las estadísticas:

```powershell
.\.venv\Scripts\python.exe infraestructura.py
```

Con el corpus original cargado, se esperan ocho vectores en `documentacion-tecnica`. Pinecone puede tardar unos segundos en reflejar la carga; en ese caso, repetir la consulta de estadísticas.

Los IDs son deterministas: repetir la carga del corpus sin modificarlo actualiza los mismos registros. La ingesta no elimina automáticamente registros correspondientes a documentos borrados o a fragmentos que dejaron de existir. Si cambia el corpus o la fragmentación, debe reconciliarse el contenido de Pinecone antes de evaluar.

## Recuperación híbrida

```powershell
.\.venv\Scripts\python.exe rag.py
```

`RAGSystem` prepara BM25 en memoria con los documentos locales y conecta el recuperador vectorial al namespace de Pinecone. Ambos recuperan hasta cinco candidatos. `EnsembleRetriever` aplica RRF con pesos `[0.5, 0.5]`, constante `c=60` y `chunk_id` como clave para reconocer duplicados. El método `buscar()` devuelve los primeros cinco fragmentos del ranking fusionado.

La tokenización léxica normaliza mayúsculas y conserva términos con puntos, como `asyncio.gather`.

Ejemplo de consulta ejecutada:

```text
Pregunta: ¿Cómo puedo manejar un error durante la ejecución sin que el programa termine inmediatamente?
Resultados híbridos: 5
1. 03_excepciones::chunk-1 | Fuente: 03_excepciones.md
2. 08_asyncio_semaforos::chunk-1 | Fuente: 08_asyncio_semaforos.md
3. 02_funciones::chunk-1 | Fuente: 02_funciones.md
4. 07_asyncio_tareas::chunk-1 | Fuente: 07_asyncio_tareas.md
5. 06_modulos::chunk-1 | Fuente: 06_modulos.md
```

Los métodos `buscar_vectorial()` y `buscar_bm25()` permiten inspeccionar cada recuperación por separado. Las búsquedas rechazan preguntas vacías.

BM25 se reconstruye desde los archivos locales: estos deben coincidir con el corpus cargado en Pinecone. Generar embeddings o consultar el índice no entrena el modelo.

## Evaluación

```powershell
.\.venv\Scripts\python.exe evaluate.py
```

El golden set contiene cinco preguntas. Cada una declara una o más fuentes relevantes mediante `doc_id`; `respuesta_esperada` explica la evidencia buscada y no se utiliza para dirigir la recuperación. El recuperador recibe solamente la pregunta.

Se evalúan documentos fuente distintos, conservando su primera aparición en el ranking. Cada fuente se cuenta una sola vez. Precision@5 divide los aciertos por cinco, incluso si faltan resultados; Recall@5 divide los aciertos por la cantidad de fuentes relevantes definidas para esa pregunta. El resumen es el promedio de las cinco métricas individuales, con igual peso por pregunta.

Resultados observados con el corpus y la configuración incluidos:

| Pregunta | Fuentes relevantes | Precision@5 | Recall@5 |
|---|---:|---:|---:|
| P1: conversión numérica y excepciones | 1 | 20 % | 100 % |
| P2: retorno de objetos y métodos | 2 | 40 % | 100 % |
| P3: concurrencia y semáforos | 2 | 40 % | 100 % |
| P4: archivos UTF-8 y cierre | 1 | 20 % | 100 % |
| P5: ejecución directa e imports | 1 | 20 % | 100 % |
| **Promedio** | | **28 %** | **100 %** |

```text
=== RESUMEN DE EVALUACIÓN ===
Preguntas evaluadas: 5
Precision@5 media: 28.00%
Recall@5 medio: 100.00%
```

El 28 % es el máximo de precisión para estas referencias y `k=5`: hay siete fuentes relevantes distribuidas entre veinticinco posiciones evaluadas. El 100 % de recall indica que se recuperaron todas las fuentes definidas como relevantes en este benchmark; no demuestra el mismo rendimiento con preguntas nuevas ni con corpus mayores.

Actualmente hay un fragmento por fuente. Si se incorporan múltiples fragmentos por documento, habrá que ampliar la recuperación de candidatos y seleccionar fuentes únicas para completar cinco fuentes después de deduplicar.

## Pruebas unitarias

```powershell
.\.venv\Scripts\python.exe -m unittest -v test_evaluate
```

Las ocho pruebas verifican recuperación completa, recuperación parcial, duplicados, ausencia de aciertos, relevantes fuera del top-k, menos resultados que k, k inválido y referencia vacía.

Salida esperada:

```text
Ran 8 tests in 0.001s

OK
```

Las pruebas no consultan los servicios externos. Los imports del proyecto sí cargan la configuración, por lo que el archivo `.env` debe tener las variables requeridas presentes.

## Fuentes del corpus

Los ocho Markdown son resúmenes didácticos originales en español basados en la [documentación oficial de Python 3.12](https://docs.python.org/3.12/). Cada documento identifica la URL específica utilizada. Los ejemplos y la selección temática se orientan al aprendizaje y a la evaluación de recuperación.
