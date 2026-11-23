# Proyecto de Listas - Carrito de compras
# Lista enlazada simple, como la vista en clase: clases NodoLista y Lista.


class NodoLista:
    # Cada nodo guarda un dato y la referencia al siguiente nodo.

    def __init__(self, objeto):
        self.datos = objeto
        self.siguienteNodo = None


class Lista:
    # Lista enlazada simple. Guarda el primer nodo y el último nodo.

    def __init__(self):
        self.primerNodo = None
        self.ultimoNodo = None

    def estaVacia(self):
        # Regresa True si la lista no tiene nodos.
        return self.primerNodo is None

    def insertarAlFinal(self, elemento):
        # Crea un nodo nuevo y lo pone después del último nodo.
        nuevo = NodoLista(elemento)
        if self.estaVacia():
            self.primerNodo = nuevo
            self.ultimoNodo = nuevo
        else:
            self.ultimoNodo.siguienteNodo = nuevo
            self.ultimoNodo = nuevo

    def eliminar(self, elemento):
        # Quita el nodo que tiene ese elemento.
        # Regresa True si lo encontró y False si no estaba en la lista.
        anterior = None
        actual = self.primerNodo
        while actual is not None:
            if actual.datos == elemento:
                if anterior is None:
                    # Es el primer nodo: ahora el primero es el siguiente.
                    self.primerNodo = actual.siguienteNodo
                else:
                    # Está en medio o al final: se liga el anterior con el siguiente.
                    anterior.siguienteNodo = actual.siguienteNodo
                if actual == self.ultimoNodo:
                    # Si era el último, ahora el último es el anterior.
                    self.ultimoNodo = anterior
                return True
            anterior = actual
            actual = actual.siguienteNodo
        return False

    def vaciar(self):
        # Deja la lista sin nodos.
        self.primerNodo = None
        self.ultimoNodo = None
