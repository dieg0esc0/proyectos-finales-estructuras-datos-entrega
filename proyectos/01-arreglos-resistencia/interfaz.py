# Proyecto de Arreglos - Resistencia eléctrica
# Versión gráfica del programa hecha con Tkinter.

import tkinter as tk
from tkinter import messagebox
from resistencia import Resistencia, Circuito, COLORES, COLORES_ESPECIALES, MAXIMO_N

# Arreglo con el color que se pinta en la pantalla para cada banda.
# Está en el mismo orden que el arreglo COLORES.
PINTURA = ["black", "saddlebrown", "red", "orange", "yellow",
           "green", "blue", "purple", "gray", "white"]

# Colores de pantalla para Dorado y Plateado, en el mismo orden que COLORES_ESPECIALES.
PINTURA_ESPECIAL = ["gold", "silver"]


class VentanaResistencia:
    # Ventana del programa: arriba los colores (R1) y abajo serie y paralelo (R2 y R3).

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Proyecto Arreglos - Resistencia eléctrica")

        titulo = tk.Label(raiz, text="Resistencia eléctrica", font=("Arial", 20, "bold"))
        titulo.pack(pady=10)

        self.crear_seccion_colores()
        self.crear_seccion_circuito()
        self.mostrar_colores()

    # ------------------------- R1: colores -------------------------

    def crear_seccion_colores(self):
        # Crea la caja de texto, el botón y el dibujo de la resistencia.
        marco = tk.LabelFrame(self.raiz, text="R1 - Colores de la resistencia")
        marco.pack(padx=10, pady=5)

        tk.Label(marco, text="Valor (ohmios):").pack()
        self.entrada_valor = tk.Entry(marco)
        self.entrada_valor.insert(0, "160")
        self.entrada_valor.pack()

        boton = tk.Button(marco, text="Obtener colores", command=self.mostrar_colores)
        boton.pack(pady=5)

        self.lienzo = tk.Canvas(marco, width=500, height=180, bg="white")
        self.lienzo.pack()

        self.etiqueta_colores = tk.Label(marco, text="", font=("Arial", 14))
        self.etiqueta_colores.pack(pady=5)

    def mostrar_colores(self):
        # Lee el valor, calcula los colores y los muestra con texto y con el dibujo.
        texto = self.entrada_valor.get()
        try:
            valor = float(texto)
        except ValueError:
            messagebox.showerror("Dato no válido", "Escribe un número, por ejemplo 160, 5800, 4.7 o 0.47.")
            return

        resistencia = Resistencia(valor)
        if resistencia.calcular_colores():
            self.dibujar_resistencia(resistencia.bandas)
            self.etiqueta_colores.config(text=texto + " ohmios = " + resistencia.texto_colores(), fg="black")
        else:
            self.lienzo.delete("all")
            self.etiqueta_colores.config(text=resistencia.error, fg="red")

    def dibujar_resistencia(self, bandas):
        # Dibuja el cuerpo de la resistencia y un rectángulo de color por cada banda.
        self.lienzo.delete("all")
        self.lienzo.create_line(20, 90, 480, 90, width=5, fill="gray")
        self.lienzo.create_rectangle(130, 50, 370, 130, fill="tan")

        for i in range(len(bandas)):
            x = 170 + i * 60
            if bandas[i] in COLORES:
                color = PINTURA[COLORES.index(bandas[i])]
            else:
                color = PINTURA_ESPECIAL[COLORES_ESPECIALES.index(bandas[i])]
            self.lienzo.create_rectangle(x, 50, x + 25, 130, fill=color)
            self.lienzo.create_text(x + 12, 150, text=bandas[i])

    # ---------------------- R2 y R3: serie y paralelo ----------------------

    def crear_seccion_circuito(self):
        # Crea la caja para n, la lista de resistores y las etiquetas de resultados.
        marco = tk.LabelFrame(self.raiz, text="R2 y R3 - Resistencias en serie y en paralelo")
        marco.pack(padx=10, pady=5)

        tk.Label(marco, text="Cantidad de resistencias (n):").pack()
        self.entrada_n = tk.Entry(marco)
        self.entrada_n.insert(0, "5")
        self.entrada_n.pack()

        boton = tk.Button(marco, text="Generar y calcular", command=self.calcular_circuito)
        boton.pack(pady=5)

        self.lista_resistores = tk.Listbox(marco, width=45, height=8)
        self.lista_resistores.pack()

        self.etiqueta_serie = tk.Label(marco, text="")
        self.etiqueta_serie.pack()
        self.etiqueta_inversos = tk.Label(marco, text="")
        self.etiqueta_inversos.pack()
        self.etiqueta_paralelo = tk.Label(marco, text="")
        self.etiqueta_paralelo.pack(pady=5)

    def calcular_circuito(self):
        # Revisa n, genera los resistores y muestra los totales en serie y en paralelo.
        texto = self.entrada_n.get()
        # isdecimal() solo acepta dígitos que int() sí puede convertir (isdigit() también acepta ²).
        if not texto.isdecimal() or int(texto) < 1 or int(texto) > MAXIMO_N:
            messagebox.showerror("Dato no válido", "n debe ser un número entero entre 1 y " + str(MAXIMO_N) + ".")
            return

        n = int(texto)
        circuito = Circuito(n)
        circuito.generar_resistores()

        self.lista_resistores.delete(0, "end")
        for i in range(n):
            self.lista_resistores.insert("end", "R" + str(i + 1) + " = " + str(circuito.resistores[i]) + " ohmios")

        self.etiqueta_serie.config(text="Serie: Rts = " + str(circuito.total_serie()) + " ohmios")
        self.etiqueta_inversos.config(text="Suma de inversos (resultado intermedio): 1/R1 + ... + 1/R" + str(n)
                                      + " = " + str(circuito.suma_inversos()))
        self.etiqueta_paralelo.config(text="Paralelo: Rtp = 1 / (suma de inversos) = "
                                      + str(round(circuito.total_paralelo(), 2)) + " ohmios")


if __name__ == "__main__":
    ventana_principal = tk.Tk()
    interfaz = VentanaResistencia(ventana_principal)
    ventana_principal.mainloop()
