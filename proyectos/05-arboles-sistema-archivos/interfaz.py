import tkinter as tk
from tkinter import ttk
from sistema_archivos import SistemaArchivos


class InterfazSistemaArchivos:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Archivos ABB")
        self.ventana.geometry("1000x650")
        self.sistema = SistemaArchivos("Documentos")
        morado = "#603BA0"

        encabezado = tk.Label(
            self.ventana,
            text="Sistema de Archivos con Árbol Binario de Búsqueda",
            bg=morado,
            fg="white",
            font=("TkDefaultFont", 20, "bold"),
            pady=16,
        )
        encabezado.pack(fill=tk.X)

        centro = tk.Frame(self.ventana, padx=20, pady=16)
        centro.pack(fill=tk.BOTH, expand=True)

        panel = tk.Frame(centro)
        panel.pack(side=tk.LEFT, anchor=tk.N, padx=(0, 20))

        tk.Label(panel, text="NUEVO ELEMENTO", font=("TkDefaultFont", 13, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        tk.Label(panel, text="Nombre").grid(row=1, column=0, sticky=tk.W, pady=6)
        self.entrada_nombre = tk.Entry(panel, width=20)
        self.entrada_nombre.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0))

        tk.Label(panel, text="Tipo").grid(row=2, column=0, sticky=tk.W, pady=6)
        self.tipo_elemento = tk.StringVar(self.ventana, value="Directorio")
        selector_tipo = tk.OptionMenu(
            panel, self.tipo_elemento, "Directorio", "Archivo", command=self.actualizar_campos
        )
        selector_tipo.config(takefocus=True)
        selector_tipo.grid(row=2, column=1, sticky=tk.EW, padx=(10, 0))

        tk.Label(panel, text="Extensión").grid(row=3, column=0, sticky=tk.W, pady=6)
        self.entrada_extension = tk.Entry(panel, width=20)
        self.entrada_extension.grid(row=3, column=1, sticky=tk.EW, padx=(10, 0))

        tk.Label(panel, text="Tamaño").grid(row=4, column=0, sticky=tk.W, pady=6)
        self.entrada_tamano = tk.Entry(panel, width=20)
        self.entrada_tamano.grid(row=4, column=1, sticky=tk.EW, padx=(10, 0))

        estilo = ttk.Style(self.ventana)
        estilo.theme_use("clam")
        estilo.configure("Insertar.TButton", background=morado, foreground="white", padding=6)
        estilo.map("Insertar.TButton", background=[("active", "#4D2B84")])
        boton_insertar = ttk.Button(
            panel, text="Insertar", style="Insertar.TButton", command=self.insertar_elemento
        )
        boton_insertar.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=(12, 0))

        self.canvas_arbol = tk.Canvas(
            centro, bg="white", highlightthickness=1, highlightbackground="#8E96A7"
        )
        self.canvas_arbol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inferior = tk.Frame(self.ventana, padx=20)
        inferior.pack(fill=tk.X, pady=(0, 16))

        self.resultados = tk.Text(
            inferior, wrap=tk.WORD, height=6, bg="#24212B", fg="white", state=tk.DISABLED
        )
        self.resultados.pack(fill=tk.X, pady=(0, 8))

        boton_salir = tk.Button(inferior, text="Salir", command=self.ventana.destroy)
        boton_salir.pack(anchor=tk.E)

        self.actualizar_campos(self.tipo_elemento.get())
        self.canvas_arbol.bind("<Configure>", self.dibujar_raiz)
        self.ventana.update_idletasks()
        self.dibujar_raiz()

    def actualizar_campos(self, tipo_seleccionado):
        self.entrada_extension.config(state=tk.NORMAL)
        self.entrada_tamano.config(state=tk.NORMAL)

        if tipo_seleccionado == "Directorio":
            self.entrada_extension.delete(0, tk.END)
            self.entrada_tamano.delete(0, tk.END)
            self.entrada_extension.config(state=tk.DISABLED)
            self.entrada_tamano.config(state=tk.DISABLED)

    def insertar_elemento(self):
        nombre = self.entrada_nombre.get()
        tipo = self.tipo_elemento.get()

        if tipo == "Directorio":
            mensaje = self.sistema.insertar_directorio(nombre)
        else:
            extension = self.entrada_extension.get()
            try:
                tamano = int(self.entrada_tamano.get())
            except ValueError:
                self.mostrar_mensaje("El tamaño debe ser un número entero.")
                return

            mensaje = self.sistema.insertar_archivo(nombre, extension, tamano)

        self.mostrar_mensaje(mensaje)
        if mensaje.endswith("insertado correctamente."):
            self.entrada_nombre.delete(0, tk.END)
            if tipo == "Archivo":
                self.entrada_extension.delete(0, tk.END)
                self.entrada_tamano.delete(0, tk.END)

    def dibujar_raiz(self, evento=None):
        canvas = self.canvas_arbol
        canvas.delete("all")
        raiz = self.sistema.raiz
        centro_x = canvas.winfo_width() // 2

        canvas.create_rectangle(
            centro_x - 100, 30, centro_x + 100, 78, fill="#DDEEFF", outline="#5286BC"
        )
        canvas.create_text(
            centro_x, 54, text=f"Directorio: {raiz.nombre}", fill="#173654"
        )

    def mostrar_mensaje(self, mensaje):
        self.resultados.config(state=tk.NORMAL)
        self.resultados.delete("1.0", tk.END)
        self.resultados.insert("1.0", mensaje)
        self.resultados.config(state=tk.DISABLED)


if __name__ == "__main__":
    ventana = tk.Tk()
    interfaz = InterfazSistemaArchivos(ventana)
    ventana.mainloop()
