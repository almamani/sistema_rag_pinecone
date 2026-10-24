# Corrutinas, gather y límites de tiempo

Versión de referencia: Python 3.12.
Categoría: python.
Tipo de material: resumen didáctico original basado en documentación oficial; no es una copia íntegra.
Fuente: https://docs.python.org/3.12/library/asyncio-task.html

async def define una función de corrutina. Llamarla crea un objeto corrutina, pero no basta para ejecutarla. asyncio.run puede iniciar la corrutina principal desde un programa síncrono. await espera el resultado de una operación esperable.

asyncio.gather permite ejecutar concurrentemente varias operaciones esperables y devuelve los resultados en el orden de los argumentos, aunque terminen en otro orden. Con return_exceptions=True, las excepciones se incluyen entre los resultados para poder inspeccionarlas.

asyncio.sleep suspende la tarea actual y permite que avancen otras. Declarar async def no convierte automáticamente una operación bloqueante en una llamada no bloqueante.

Ejemplo:
```python
import asyncio

async def consultar(nombre):
    await asyncio.sleep(0.1)
    return nombre

async def main():
    resultados = await asyncio.gather(
        consultar("ventas"),
        consultar("stock"),
    )
    print(resultados)

asyncio.run(main())
```

asyncio.timeout establece un plazo para un bloque asíncrono y transforma la cancelación por vencimiento en TimeoutError fuera del contexto. Estos límites ayudan a evitar esperas indefinidas. La concurrencia cooperativa no implica ejecutar código Python de CPU en paralelo.

