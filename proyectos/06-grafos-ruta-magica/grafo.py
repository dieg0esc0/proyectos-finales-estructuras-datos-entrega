from carretera import Carretera
from pueblo import Pueblo


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
                
                if origen <= carretera.destino:
                    carreteras.append([origen, carretera.destino, carretera.distancia])
        return carreteras

    def cargar_pueblos(self, archivo):
        with open(archivo, encoding="utf-8") as datos:
            for linea in datos:
                
                linea = linea.strip()
                if not linea or linea.startswith("#"):
                    continue

                nombre, x, y = linea.split()
                pueblo = Pueblo(nombre, int(x), int(y))
                self.agregar_pueblo(pueblo)

    def cargar_carreteras(self, archivo):
        with open(archivo, encoding="utf-8") as datos:
            for linea in datos:
                linea = linea.strip()
                if not linea or linea.startswith("#"):
                    continue

                origen, destino, distancia = linea.split()
                
                self.agregar_carretera(origen, destino, int(distancia))
