# Semáforos y control de concurrencia

Versión de referencia: Python 3.12.
Categoría: python.
Tipo de material: resumen didáctico original basado en documentación oficial; no es una copia íntegra.
Fuente: https://docs.python.org/3.12/library/asyncio-sync.html

asyncio.Semaphore limita cuántas tareas pueden acceder simultáneamente a una sección de código. Mantiene un contador que disminuye al adquirir un permiso y aumenta al liberarlo. Cuando llega a cero, nuevas adquisiciones esperan.

El uso recomendado es async with semaforo. La salida del contexto libera el permiso, incluso si se produce una excepción en el bloque. Un mismo semáforo compartido debe utilizarse en las tareas que se quieren coordinar.

Ejemplo:
```python
import asyncio

async def main():
    semaforo = asyncio.Semaphore(2)

    async def consultar(numero):
        async with semaforo:
            await asyncio.sleep(0.1)
            return numero

    resultados = await asyncio.gather(
        *(consultar(n) for n in range(5))
    )
    print(resultados)

asyncio.run(main())
```

Se crean cinco operaciones, pero como máximo dos permanecen dentro de la sección protegida al mismo tiempo. El semáforo no significa dos llamadas por segundo: controla concurrencia, no una tasa temporal de solicitudes.

Las primitivas de sincronización de asyncio coordinan tareas del entorno asíncrono y no deben usarse como mecanismos de sincronización entre hilos del sistema operativo. Un Lock permite acceso exclusivo; un Event permite notificar a tareas que esperan una señal.

