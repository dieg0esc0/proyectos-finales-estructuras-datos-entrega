from ruta import Ruta


INFINITO = float("inf")


class Dijkstra:
    def __init__(self, grafo):
        self.grafo = grafo

    def calcular(self, origen, destino):
        distancias = {}
        anteriores = {}
        visitados = []

        for nombre in self.grafo.nombres_pueblos():
            distancias[nombre] = INFINITO
            anteriores[nombre] = None

        if origen not in distancias or destino not in distancias:
            return Ruta([], [], 0)

        distancias[origen] = 0
        actual = self.mas_cercano(distancias, visitados)

        while actual is not None:
            visitados.append(actual)

            # Actualiza la mejor distancia conocida a cada vecino.
            for carretera in self.grafo.vecinos(actual):
                vecino = carretera.destino
                distancia_nueva = distancias[actual] + carretera.distancia
                if distancia_nueva < distancias[vecino]:
                    distancias[vecino] = distancia_nueva
                    anteriores[vecino] = actual

            actual = self.mas_cercano(distancias, visitados)

        return self.armar_ruta(anteriores, distancias, origen, destino)

    def mas_cercano(self, distancias, visitados):
        cercano = None
        distancia_minima = INFINITO

        for nombre, distancia in distancias.items():
            if nombre not in visitados and distancia < distancia_minima:
                cercano = nombre
                distancia_minima = distancia

        return cercano

    def armar_ruta(self, anteriores, distancias, origen, destino):
        if distancias.get(destino, INFINITO) == INFINITO:
            return Ruta([], [], 0)

        # Sigue los pueblos anteriores y luego invierte el recorrido.
        pueblos = [destino]
        actual = destino
        while actual != origen:
            actual = anteriores[actual]
            pueblos.append(actual)
        pueblos.reverse()

        tramos = []
        for indice in range(len(pueblos) - 1):
            inicio = pueblos[indice]
            fin = pueblos[indice + 1]
            kilometros = self.grafo.distancia_directa(inicio, fin)
            tramos.append([inicio, fin, kilometros])

        return Ruta(pueblos, tramos, distancias[destino])
