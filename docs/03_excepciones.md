# Manejo de errores y excepciones

Versión de referencia: Python 3.12.
Categoría: python.
Tipo de material: resumen didáctico original basado en documentación oficial; no es una copia íntegra.
Fuente: https://docs.python.org/3.12/tutorial/errors.html

Una excepción representa un error detectado durante la ejecución. Puede ocurrir aunque el programa tenga sintaxis válida. ValueError indica, por ejemplo, que una conversión recibió un valor inadecuado; ZeroDivisionError corresponde a una división por cero.

try delimita operaciones que pueden fallar. except maneja excepciones del tipo indicado. Si no hay un manejador compatible, la excepción se propaga. Capturar tipos concretos permite distinguir fallos esperados de errores inesperados.

else se ejecuta cuando el bloque try termina sin excepción. finally permite realizar limpieza tanto si hubo un error como si no. raise permite lanzar una excepción de manera explícita para informar una condición inválida.

Ejemplo:
```python
def convertir_precio(texto):
    try:
        precio = float(texto)
    except ValueError as error:
        raise ValueError("El precio debe ser numérico") from error

    if precio < 0:
        raise ValueError("El precio no puede ser negativo")

    return precio
```

La validación diferencia una conversión fallida de un número negativo. from conserva la relación con la excepción original. Un mensaje claro ayuda al llamador a comprender por qué no pudo completarse la operación.

