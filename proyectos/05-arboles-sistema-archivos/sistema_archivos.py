from nodo import Nodo


class SistemaArchivos:
    def __init__(self, nombre_raiz):
        self.raiz = Nodo(nombre_raiz, "", 0, "Directorio")

    def mostrar_raiz(self):
        return self.raiz.obtener_informacion()

    def insertar_directorio(self, nombre):
        nuevo = Nodo(nombre, "", 0, "Directorio")
        return self._insertar_nodo(nuevo)

    def insertar_archivo(self, nombre, extension, tamano):
        nuevo = Nodo(nombre, extension, tamano, "Archivo")
        return self._insertar_nodo(nuevo)

    def _insertar_nodo(self, nuevo):
        actual = self.raiz
        nombre_nuevo = nuevo.nombre.lower()

        while True:
            nombre_actual = actual.nombre.lower()

            if nombre_nuevo == nombre_actual:
                return f"No se pudo insertar '{nuevo.nombre}': el nombre ya existe."

            if actual.tipo == "Archivo":
                return (
                    f"No se pudo insertar '{nuevo.nombre}': "
                    f"el archivo '{actual.nombre}' no puede contener otros elementos."
                )

            if nombre_nuevo < nombre_actual:
                if actual.hijo_izquierdo is None:
                    actual.hijo_izquierdo = nuevo
                    return f"{nuevo.tipo} '{nuevo.nombre}' insertado correctamente."
                actual = actual.hijo_izquierdo
            else:
                if actual.hijo_derecho is None:
                    actual.hijo_derecho = nuevo
                    return f"{nuevo.tipo} '{nuevo.nombre}' insertado correctamente."
                actual = actual.hijo_derecho

    def buscar(self, nombre):
        actual = self.raiz
        nombre_buscado = nombre.lower()

        while actual is not None:
            nombre_actual = actual.nombre.lower()

            if nombre_buscado == nombre_actual:
                return actual

            if nombre_buscado < nombre_actual:
                actual = actual.hijo_izquierdo
            else:
                actual = actual.hijo_derecho

        return None

    def recorrido_inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo is None:
            return

        self._inorden(nodo.hijo_izquierdo, resultado)
        resultado.append(nodo)
        self._inorden(nodo.hijo_derecho, resultado)

    def recorrido_preorden(self):
        resultado = []
        self._preorden(self.raiz, resultado)
        return resultado

    def _preorden(self, nodo, resultado):
        if nodo is None:
            return

        resultado.append(nodo)
        self._preorden(nodo.hijo_izquierdo, resultado)
        self._preorden(nodo.hijo_derecho, resultado)

    def recorrido_postorden(self):
        resultado = []
        self._postorden(self.raiz, resultado)
        return resultado

    def _postorden(self, nodo, resultado):
        if nodo is None:
            return

        self._postorden(nodo.hijo_izquierdo, resultado)
        self._postorden(nodo.hijo_derecho, resultado)
        resultado.append(nodo)


    def eliminar(self, nombre):
        encontrado = self.buscar(nombre)

        if encontrado is None:
            return f"No se pudo eliminar '{nombre}': el elemento no existe."

        if encontrado is self.raiz:
            return f"No se pudo eliminar '{nombre}': es la raíz del árbol."

        tiene_hijos = (
            encontrado.hijo_izquierdo is not None
            or encontrado.hijo_derecho is not None
        )
        if encontrado.tipo == "Directorio" and tiene_hijos:
            return f"No se pudo eliminar '{nombre}': el directorio tiene hijos."

        self.raiz = self._eliminar_nodo(self.raiz, nombre)
        return f"{encontrado.tipo} '{encontrado.nombre}' eliminado correctamente."

    def _eliminar_nodo(self, nodo, nombre):
        if nodo is None:
            return None

        nombre_buscado = nombre.lower()
        nombre_actual = nodo.nombre.lower()

        if nombre_buscado < nombre_actual:
            nodo.hijo_izquierdo = self._eliminar_nodo(nodo.hijo_izquierdo, nombre)
        elif nombre_buscado > nombre_actual:
            nodo.hijo_derecho = self._eliminar_nodo(nodo.hijo_derecho, nombre)
        else:
            if nodo.hijo_izquierdo is None and nodo.hijo_derecho is None:
                return None

            if nodo.hijo_izquierdo is None:
                return nodo.hijo_derecho
            if nodo.hijo_derecho is None:
                return nodo.hijo_izquierdo

            sucesor = self._buscar_menor(nodo.hijo_derecho)
            nodo.nombre = sucesor.nombre
            nodo.extension = sucesor.extension
            nodo.tamano = sucesor.tamano
            nodo.tipo = sucesor.tipo
            nodo.hijo_derecho = self._eliminar_nodo(nodo.hijo_derecho, sucesor.nombre)

        return nodo

    def _buscar_menor(self, nodo):
        while nodo.hijo_izquierdo is not None:
            nodo = nodo.hijo_izquierdo
        return nodo
