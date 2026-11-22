from pila import Pila
from urls import clave_pagina

CAPACIDAD = 4


class Navegador:
    def __init__(self):
        self.pila_atras = Pila(CAPACIDAD)
        self.pila_adelante = Pila(CAPACIDAD)
        self.pagina_actual = None
        self.registro = []

    def es_la_misma(self, url):
        if self.pagina_actual is None:
            return False
        return clave_pagina(self.pagina_actual) == clave_pagina(url)

    def visitar(self, url):
        if self.es_la_misma(url):
            return "MISMA"
        if self.pagina_actual is not None:
            if self.pila_atras.esta_llena():
                return "LLENA"
            self.pila_atras.push(self.pagina_actual)
            self.registro.append("PUSH Pila atrás  <-  " + self.pagina_actual)
        if not self.pila_adelante.esta_vacia():
            cantidad = self.pila_adelante.tamano
            self.pila_adelante.vaciar()
            self.registro.append("Pila adelante vaciada (" + str(cantidad) + " páginas)")
        self.pagina_actual = url
        self.registro.append("VISITAR  " + url)
        return "OK"

    def retroceder(self):
        if self.pila_atras.esta_vacia():
            return "VACIA"
        if self.pila_adelante.esta_llena():
            return "LLENA"
        self.pila_adelante.push(self.pagina_actual)
        self.registro.append("PUSH Pila adelante  <-  " + self.pagina_actual)
        self.pagina_actual = self.pila_atras.pop()
        self.registro.append("POP Pila atrás  ->  " + self.pagina_actual)
        return "OK"

    def avanzar(self):
        if self.pila_adelante.esta_vacia():
            return "VACIA"
        if self.pila_atras.esta_llena():
            return "LLENA"
        self.pila_atras.push(self.pagina_actual)
        self.registro.append("PUSH Pila atrás  <-  " + self.pagina_actual)
        self.pagina_actual = self.pila_adelante.pop()
        self.registro.append("POP Pila adelante  ->  " + self.pagina_actual)
        return "OK"
