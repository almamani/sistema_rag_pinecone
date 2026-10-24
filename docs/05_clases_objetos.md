# Clases, instancias, atributos y métodos

Versión de referencia: Python 3.12.
Categoría: python.
Tipo de material: resumen didáctico original basado en documentación oficial; no es una copia íntegra.
Fuente: https://docs.python.org/3.12/tutorial/classes.html

Una clase agrupa datos y comportamiento. Al llamar a la clase se crea una instancia. Si se define __init__, Python lo invoca para inicializar esa instancia con los argumentos recibidos.

Los atributos conservan el estado del objeto. Los métodos son funciones definidas en la clase que pueden operar sobre ese estado. Por convención, el primer parámetro de un método de instancia se llama self. Al invocar objeto.metodo(), la instancia se proporciona implícitamente a ese parámetro.

Ejemplo:
```python
class Catalogo:
    def __init__(self, nombre):
        self.nombre = nombre

    def describir(self):
        return f"Catálogo: {self.nombre}"

def crear_catalogo():
    return Catalogo("Python")

catalogo = crear_catalogo()
mensaje = catalogo.describir()
```

crear_catalogo devuelve un objeto. La variable catalogo recibe esa instancia y luego permite llamar a su método describir. La función creadora no ejecuta ese método por el hecho de devolver el objeto.

Los atributos de instancia pueden mantener datos distintos para cada objeto. Los atributos de clase pertenecen a la clase y pueden ser compartidos. Utilizar una lista mutable de clase para datos que deberían ser individuales puede compartir cambios accidentalmente.

