import os
import tkinter as tk

from grafo import Grafo
from ventana import VentanaRutaMagica


def main():
    carpeta = os.path.dirname(os.path.abspath(__file__))
    grafo = Grafo()
    grafo.cargar_pueblos(os.path.join(carpeta, "pueblos.txt"))
    grafo.cargar_carreteras(os.path.join(carpeta, "carreteras.txt"))

    raiz = tk.Tk()
    VentanaRutaMagica(raiz, grafo)
    raiz.mainloop()


if __name__ == "__main__":
    main()
