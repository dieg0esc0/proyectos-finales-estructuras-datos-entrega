import tkinter as tk
from tkinter import messagebox, ttk

from dijkstra import Dijkstra


class VentanaRutaMagica:
    def __init__(self, raiz, grafo):
        self.raiz = raiz
        self.grafo = grafo
        self.dijkstra = Dijkstra(grafo)

        self.raiz.title("Ruta Mágica - Pueblos Mágicos de Yucatán")
        self.raiz.geometry("1000x560")
        self.raiz.minsize(960, 490)

        self.pestanas = ttk.Notebook(raiz)
        self.pestanas.pack(fill="both", expand=True, padx=16, pady=16)
        self.pagina_ruta = ttk.Frame(self.pestanas, padding=12)
        self.pagina_matriz = ttk.Frame(self.pestanas, padding=12)
        self.pestanas.add(self.pagina_ruta, text="Buscar ruta")
        self.pestanas.add(self.pagina_matriz, text="Matriz de adyacencia")

        self.crear_mapa()
        self.crear_panel()
        self.crear_matriz()
        self.dibujar_grafo()

    def crear_mapa(self):
        self.mapa = tk.Canvas(
            self.pagina_ruta, width=620, height=410,
            background="#f5faf8", highlightthickness=1,
            highlightbackground="#c9d8d3",
        )
        self.mapa.pack(side="left", fill="both", expand=True, padx=(0, 16))

    def crear_panel(self):
        panel = ttk.Frame(self.pagina_ruta)
        panel.pack(side="right", fill="y")
        nombres = self.grafo.nombres_pueblos()

        ttk.Label(panel, text="Pueblo de origen").pack(anchor="w")
        self.origen = ttk.Combobox(panel, values=nombres, state="readonly")
        self.origen.pack(fill="x", pady=(4, 12))

        ttk.Label(panel, text="Pueblo de destino").pack(anchor="w")
        self.destino = ttk.Combobox(panel, values=nombres, state="readonly")
        self.destino.pack(fill="x", pady=(4, 12))

        botones = ttk.Frame(panel)
        botones.pack(fill="x", pady=(0, 16))
        ttk.Button(botones, text="Calcular ruta", command=self.calcular_ruta).pack(side="left")
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=8)

        ttk.Label(panel, text="Resultado").pack(anchor="w", pady=(0, 4))
        self.resultado = tk.Text(
            panel, width=34, height=12, wrap="word", state="disabled",
            font="TkDefaultFont", padx=10, pady=8,
        )
        self.resultado.pack(fill="both", expand=True)

    def crear_matriz(self):
        pueblos = self.grafo.nombres_pueblos()
        self.matriz = ttk.Treeview(self.pagina_matriz, columns=pueblos, height=len(pueblos))
        self.matriz.heading("#0", text="Pueblo", anchor="w")
        self.matriz.column("#0", width=116, minwidth=90)
        for pueblo in pueblos:
            self.matriz.heading(pueblo, text=pueblo)
            self.matriz.column(pueblo, width=100, minwidth=85, anchor="center")

        
        for origen in pueblos:
            fila = []
            for destino in pueblos:
                if origen == destino:
                    fila.append(0)
                else:
                    distancia = self.grafo.distancia_directa(origen, destino)
                    fila.append("∞" if distancia is None else distancia)
            self.matriz.insert("", "end", text=origen, values=fila)

        self.matriz.pack(fill="both", expand=True)

    def dibujar_grafo(self, tramos=()):
        self.mapa.delete("all")
        etiquetas = []

        
        for origen, destino, distancia in self.grafo.lista_carreteras():
            inicio = self.grafo.pueblos[origen]
            fin = self.grafo.pueblos[destino]
            en_ruta = self.esta_en_ruta(origen, destino, tramos)
            color = "#b91c1c" if en_ruta else "#526b64"
            self.mapa.create_line(
                inicio.x, inicio.y, fin.x, fin.y,
                fill=color, width=4 if en_ruta else 2, tags="carretera",
            )
            etiquetas.append((
                (inicio.x + fin.x) / 2, (inicio.y + fin.y) / 2,
                distancia, color,
            ))

        for x, y, distancia, color in etiquetas:
            etiqueta = self.mapa.create_text(
                x, y, text=f"{distancia} km", fill=color,
                font=("Segoe UI", 9, "bold"), tags="distancia",
            )
            x1, y1, x2, y2 = self.mapa.bbox(etiqueta)
            fondo = self.mapa.create_rectangle(
                x1 - 3, y1 - 1, x2 + 3, y2 + 1, fill="#f5faf8", outline="",
            )
            self.mapa.tag_lower(fondo, etiqueta)

        for pueblo in self.grafo.pueblos.values():
            x, y = pueblo.x, pueblo.y
            self.mapa.create_oval(
                x - 8, y - 8, x + 8, y + 8,
                fill="#0f6658", outline="white", width=2, tags="pueblo",
            )
            self.mapa.create_text(
                x, y + 20, text=pueblo.nombre, fill="#163832",
                font=("Segoe UI", 10, "bold"), tags="nombre",
            )

    def esta_en_ruta(self, origen, destino, tramos):
        for inicio, fin, _ in tramos:
            if (origen, destino) == (inicio, fin) or (origen, destino) == (fin, inicio):
                return True
        return False

    def calcular_ruta(self):
        origen = self.origen.get()
        destino = self.destino.get()
        if not origen or not destino:
            messagebox.showwarning(
                "Ruta Mágica", "Selecciona el pueblo de origen y el de destino.",
                parent=self.raiz,
            )
            return
        if origen == destino:
            messagebox.showwarning(
                "Ruta Mágica", "El origen y el destino deben ser pueblos diferentes.",
                parent=self.raiz,
            )
            return

        ruta = self.dijkstra.calcular(origen, destino)
        if ruta.encontrada():
            lineas = ["RUTA ENCONTRADA", ""]
            for inicio, fin, distancia in ruta.tramos:
                lineas.append(f"{inicio} --({distancia} km)--> {fin}")
            lineas.extend([
                "", "Ruta completa:", ruta.texto_ruta(), "",
                f"Distancia total: {ruta.distancia_total} km",
            ])
            self.escribir_resultado("\n".join(lineas))
        else:
            self.escribir_resultado("No se encontró conexión entre los pueblos.")

        self.dibujar_grafo(ruta.tramos)

    def escribir_resultado(self, texto):
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", texto)
        self.resultado.configure(state="disabled")

    def limpiar(self):
        self.origen.set("")
        self.destino.set("")
        self.escribir_resultado("")
        self.dibujar_grafo()
