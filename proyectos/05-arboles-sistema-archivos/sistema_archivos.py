from nodo import Nodo


class SistemaArchivos:
    def __init__(self, nombre_raiz):
        if not self._nombre_valido(nombre_raiz):
            raise ValueError("El nombre de la raíz debe ser un texto no vacío.")

        self.raiz = Nodo(nombre_raiz.strip(), "", 0, "Directorio")

    def _nombre_valido(self, nombre):
        return isinstance(nombre, str) and nombre.strip() != ""

    def _extension_valida(self, extension):
        return isinstance(extension, str) and extension.strip().lstrip(".") != ""

    def mostrar_raiz(self):
        return self.raiz.obtener_informacion()

    def insertar_directorio(self, nombre):
        if not self._nombre_valido(nombre):
            return "No se pudo insertar el directorio: el nombre debe ser un texto no vacío."

        nuevo = Nodo(nombre.strip(), "", 0, "Directorio")
        return self._insertar_nodo(nuevo)

    def insertar_archivo(self, nombre, extension, tamano):
        if not self._nombre_valido(nombre):
            return "No se pudo insertar el archivo: el nombre debe ser un texto no vacío."

        if not self._extension_valida(extension):
            return "No se pudo insertar el archivo: la extensión debe ser un texto no vacío."

        if not isinstance(tamano, int) or isinstance(tamano, bool) or tamano < 0:
            return "No se pudo insertar el archivo: el tamaño debe ser un entero no negativo."

        extension = extension.strip().lstrip(".")
        nuevo = Nodo(nombre.strip(), extension, tamano, "Archivo")
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
        if not self._nombre_valido(nombre):
            return None

        actual = self.raiz
        nombre_buscado = nombre.strip().lower()

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
        if not self._nombre_valido(nombre):
            return "No se pudo eliminar: el nombre debe ser un texto no vacío."

        nombre = nombre.strip()
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
