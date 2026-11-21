class Nodo:
    def __init__(self, nombre, extension, tamano, tipo):
        if tipo not in ("Archivo", "Directorio"):
            raise ValueError("El tipo debe ser 'Archivo' o 'Directorio'.")

        self.nombre = nombre
        self.extension = extension
        self.tamano = tamano
        self.tipo = tipo
        self.hijo_izquierdo = None
        self.hijo_derecho = None

    def obtener_informacion(self):
        izquierdo = "Ninguno"
        derecho = "Ninguno"

        if self.hijo_izquierdo is not None:
            izquierdo = self.hijo_izquierdo.nombre
        if self.hijo_derecho is not None:
            derecho = self.hijo_derecho.nombre

        return (
            f"Nombre: {self.nombre}\n"
            f"Extensión: {self.extension or 'Sin extensión'}\n"
            f"Tamaño: {self.tamano}\n"
            f"Tipo: {self.tipo}\n"
            f"Hijo izquierdo: {izquierdo}\n"
            f"Hijo derecho: {derecho}"
        )
