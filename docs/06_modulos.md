# Módulos, imports y punto de entrada

Versión de referencia: Python 3.12.
Categoría: python.
Tipo de material: resumen didáctico original basado en documentación oficial; no es una copia íntegra.
Fuente: https://docs.python.org/3.12/tutorial/modules.html

Un módulo es un archivo que contiene definiciones y sentencias de Python. Permite organizar un programa y reutilizar funciones sin copiar su implementación. El nombre del archivo, sin la extensión .py, identifica normalmente el módulo.

import modulo vincula el nombre del módulo y permite acceder a sus elementos con un punto. from modulo import funcion incorpora directamente un nombre concreto. Las sentencias de nivel superior del módulo se ejecutan cuando se importa por primera vez dentro del proceso.

La variable __name__ permite distinguir una importación de la ejecución directa del archivo. Cuando se ejecuta como programa principal, su valor es "__main__". El patrón siguiente reserva una prueba para la ejecución directa.

Ejemplo:
```python
def saludar(nombre):
    return f"Hola, {nombre}"

if __name__ == "__main__":
    print(saludar("Andrea"))
```

Otro archivo puede usar from saludos import saludar sin ejecutar el print protegido. Esto permite importar funciones de infraestructura sin lanzar automáticamente su bloque de diagnóstico.

Los paquetes organizan módulos mediante nombres con puntos. Conviene elegir nombres de archivos que no oculten módulos que necesitamos importar, por ejemplo evitar llamar asyncio.py a un script de práctica.

