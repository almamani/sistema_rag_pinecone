# Funciones, argumentos y valores de retorno

Versión de referencia: Python 3.12.
Categoría: python.
Tipo de material: resumen didáctico original basado en documentación oficial; no es una copia íntegra.
Fuente: https://docs.python.org/3.12/tutorial/controlflow.html

La sentencia def define una función con un nombre y una lista de parámetros. El cuerpo se ejecuta cuando llamamos a la función. Los argumentos pueden proporcionarse por posición o por nombre. Un parámetro con valor predeterminado puede omitirse en la llamada.

return finaliza la ejecución de una función y entrega un valor al código que la llamó. Si no se ejecuta un return con una expresión, la función devuelve None. El resultado puede ser un número, una colección o un objeto.

Las variables asignadas dentro de una función pertenecen normalmente a su ámbito local. Los argumentos se vinculan a nombres locales al llamar a la función. Cambiar un objeto mutable recibido puede afectar al objeto que conserva el llamador.

Ejemplo:
```python
def calcular_precio(precio, descuento=0):
    return precio * (1 - descuento / 100)

total = calcular_precio(precio=1000, descuento=10)
```

total recibe 900.0. La expresión de llamada se resuelve antes de asignar el resultado. Conviene evitar listas o diccionarios mutables como valores predeterminados cuando se espera una colección nueva por llamada, porque el valor predeterminado se evalúa una sola vez.

