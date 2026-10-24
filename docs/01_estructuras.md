# Listas, diccionarios y conjuntos

Versión de referencia: Python 3.12.
Categoría: python.
Tipo de material: resumen didáctico original basado en documentación oficial; no es una copia íntegra.
Fuente: https://docs.python.org/3.12/tutorial/datastructures.html

Una lista conserva el orden de sus elementos y permite modificarlos. list.append agrega un elemento al final; list.extend incorpora los elementos de otro iterable. list.pop elimina y devuelve un elemento. Los índices comienzan en cero. Un slice como datos[0:2] selecciona las posiciones cero y uno. Una comprensión construye una lista a partir de un iterable.

Un diccionario relaciona claves únicas con valores. producto["precio"] obtiene el valor asociado a una clave y lanza KeyError si no existe. producto.get("precio", 0) devuelve un valor predeterminado cuando falta la clave. items() permite recorrer pares de claves y valores.

Un conjunto, o set, contiene elementos únicos y permite operaciones entre colecciones. La intersección a & b obtiene los elementos compartidos; la unión a | b combina elementos sin repetir. Los conjuntos no representan un ranking.

Ejemplo:
```python
documentos = ["A", "B", "C"]
lote = documentos[0:2]
relevantes = {"A", "D"}
aciertos = set(lote) & relevantes
```

En este ejemplo, lote contiene A y B, mientras que aciertos contiene solamente A.

