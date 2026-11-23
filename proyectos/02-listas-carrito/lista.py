# Proyecto de Listas - Carrito de compras
# Lista enlazada simple (igual que la vista en clase): NodoLista, Lista y ExcepcionListaVacia.

class NodoLista:
    """Nodo de la lista: guarda un dato y la referencia al siguiente nodo."""

    def __init__(self, objeto, nodo=None):
        self.datos = objeto
        self.siguienteNodo = nodo


class ExcepcionListaVacia(Exception):
    """Error que se lanza cuando se quiere eliminar de una lista vacía."""

    def __init__(self, nombre="Lista"):
        super().__init__(nombre + " esta vacia")


class Lista:
    """Lista enlazada simple con referencia al primer y al último nodo."""

    def __init__(self, nombreLista="lista"):
        self.nombre = nombreLista
        self.primerNodo = None
        self.ultimoNodo = None

    def estaVacia(self):
        """Regresa True si la lista no tiene nodos."""
        return self.primerNodo is None

    def insertarAlFinal(self, elementoInsertar):
        """Crea un nodo nuevo y lo liga después del último nodo."""
        if self.estaVacia():
            self.primerNodo = self.ultimoNodo = NodoLista(elementoInsertar)
        else:
            self.ultimoNodo.siguienteNodo = NodoLista(elementoInsertar)
            self.ultimoNodo = self.ultimoNodo.siguienteNodo

    def eliminarDelFrente(self):
        """Quita el primer nodo y regresa su dato."""
        if self.estaVacia():
            raise ExcepcionListaVacia(self.nombre)
        elementoEliminado = self.primerNodo.datos
        if self.primerNodo == self.ultimoNodo:
            self.primerNodo = self.ultimoNodo = None
        else:
            self.primerNodo = self.primerNodo.siguienteNodo
        return elementoEliminado

    def eliminarDelFinal(self):
        """Quita el último nodo y regresa su dato."""
        if self.estaVacia():
            raise ExcepcionListaVacia(self.nombre)
        elementoEliminado = self.ultimoNodo.datos
        if self.primerNodo == self.ultimoNodo:
            self.primerNodo = self.ultimoNodo = None
        else:
            actual = self.primerNodo
            while actual.siguienteNodo != self.ultimoNodo:
                actual = actual.siguienteNodo
            self.ultimoNodo = actual
            self.ultimoNodo.siguienteNodo = None
        return elementoEliminado

    def eliminar(self, elemento):
        """
        Elimina un elemento de cualquier posición de la lista.
        Si es el primero o el último usa los métodos anteriores; si está en medio,
        liga el nodo anterior con el nodo siguiente.
        """
        if self.estaVacia():
            raise ExcepcionListaVacia(self.nombre)
        if self.primerNodo.datos == elemento:
            return self.eliminarDelFrente()
        if self.ultimoNodo.datos == elemento:
            return self.eliminarDelFinal()
        anterior = self.primerNodo
        actual = self.primerNodo.siguienteNodo
        while actual is not None:
            if actual.datos == elemento:
                anterior.siguienteNodo = actual.siguienteNodo
                return elemento
            anterior = actual
            actual = actual.siguienteNodo
        return None

    def vaciar(self):
        """Deja la lista sin nodos."""
        self.primerNodo = self.ultimoNodo = None
