class Ruta:
    def __init__(self, pueblos, tramos, distancia_total):
        self.pueblos = pueblos
        self.tramos = tramos
        self.distancia_total = distancia_total

    def encontrada(self):
        return bool(self.pueblos)

    def texto_ruta(self):
        return " -> ".join(self.pueblos)
