from carretera import Carretera


class Grafo:
    def __init__(self):
        self.pueblos = {}
        self.adyacencia = {}

    def agregar_pueblo(self, pueblo):
        self.pueblos[pueblo.nombre] = pueblo
        self.adyacencia.setdefault(pueblo.nombre, [])

    def agregar_carretera(self, origen, destino, distancia):
        carreteras_origen = self.adyacencia[origen]
        carreteras_destino = self.adyacencia[destino]

        # Una carretera se puede recorrer en ambos sentidos.
        carreteras_origen.append(Carretera(destino, distancia))
        if origen != destino:
            carreteras_destino.append(Carretera(origen, distancia))

    def vecinos(self, nombre):
        return self.adyacencia.get(nombre, [])

    def nombres_pueblos(self):
        return list(self.pueblos)

    def distancia_directa(self, origen, destino):
        for carretera in self.vecinos(origen):
            if carretera.destino == destino:
                return carretera.distancia
        return None

    def lista_carreteras(self):
        carreteras = []
        for origen, vecinas in self.adyacencia.items():
            for carretera in vecinas:
                # El orden de los nombres permite mostrar un solo sentido.
                if origen <= carretera.destino:
                    carreteras.append([origen, carretera.destino, carretera.distancia])
        return carreteras
