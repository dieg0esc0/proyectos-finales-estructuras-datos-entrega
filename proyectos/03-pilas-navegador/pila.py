class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Pila:
    def __init__(self, capacidad):
        self.tope = None
        self.tamano = 0
        self.capacidad = capacidad

    def esta_vacia(self):
        return self.tope is None

    def esta_llena(self):
        return self.tamano == self.capacidad

    def push(self, dato):
        if self.esta_llena():
            return False
        nuevo = Nodo(dato)
        nuevo.siguiente = self.tope
        self.tope = nuevo
        self.tamano = self.tamano + 1
        return True

    def pop(self):
        if self.esta_vacia():
            return None
        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self.tamano = self.tamano - 1
        return dato

    def peek(self):
        if self.esta_vacia():
            return None
        return self.tope.dato

    def vaciar(self):
        while not self.esta_vacia():
            self.pop()

    def obtener_elementos(self):
        elementos = []
        actual = self.tope
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos
