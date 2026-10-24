# Lectura y escritura de archivos de texto

Versión de referencia: Python 3.12.
Categoría: python.
Tipo de material: resumen didáctico original basado en documentación oficial; no es una copia íntegra.
Fuente: https://docs.python.org/3.12/tutorial/inputoutput.html

open permite abrir un archivo e indicar un modo de acceso. El modo r lee; w escribe y trunca un archivo existente; a agrega contenido al final. Al trabajar con texto, indicar encoding="utf-8" evita depender de la codificación predeterminada del sistema.

La sentencia with administra el contexto del archivo y lo cierra al salir del bloque, incluso si se produce una excepción. read() obtiene el contenido completo; recorrer el archivo con for permite procesar sus líneas. write() escribe una cadena y no agrega automáticamente un salto de línea.

Ejemplo:
```python
with open("documento.md", "r", encoding="utf-8") as archivo:
    contenido = archivo.read()

with open("resumen.txt", "w", encoding="utf-8") as archivo:
    archivo.write(contenido)
```

El segundo bloque reemplaza el contenido previo de resumen.txt. Para conservar lo anterior y agregar texto se utiliza el modo a.

El módulo json permite serializar y reconstruir estructuras compatibles con JSON. json.dump escribe en un archivo y json.load lee desde uno. El archivo de preguntas de evaluación puede almacenar listas y diccionarios sin ejecutar código Python.

