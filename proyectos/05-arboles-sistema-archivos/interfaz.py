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

        estilo.configure("Buscar.TButton", background="#28744E", foreground="white", padding=6)
        estilo.map("Buscar.TButton", background=[("active", "#205E3F")])
        estilo.configure("Eliminar.TButton", background="#AD353E", foreground="white", padding=6)
        estilo.map("Eliminar.TButton", background=[("active", "#892A32")])
        estilo.configure("Cancelar.TButton", background="#626873", foreground="white", padding=6)
        estilo.map("Cancelar.TButton", background=[("active", "#4C515A")])

        ttk.Button(
            panel, text="Buscar", style="Buscar.TButton", command=self.abrir_busqueda
        ).grid(row=6, column=0, columnspan=2, sticky=tk.EW, pady=(8, 0))
        ttk.Button(
            panel, text="Eliminar", style="Eliminar.TButton", command=self.abrir_eliminacion
        ).grid(row=7, column=0, columnspan=2, sticky=tk.EW, pady=(8, 0))

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

        self.ventana.protocol("WM_DELETE_WINDOW", self.abrir_despedida)
        boton_salir = tk.Button(inferior, text="Salir", command=self.abrir_despedida)
        boton_salir.pack(anchor=tk.E)

        self.actualizar_campos(self.tipo_elemento.get())
        self.canvas_arbol.bind("<Configure>", self.dibujar_arbol)
        self.ventana.update_idletasks()
        self.dibujar_arbol()

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
            self.dibujar_arbol()

    def dibujar_arbol(self, evento=None):
        canvas = self.canvas_arbol
        canvas.delete("all")
        ancho = canvas.winfo_width()
        centro_x = ancho // 2
        separacion = max(80, ancho // 4)

        self._dibujar_nodo(self.sistema.raiz, centro_x, 54, separacion)
        canvas.tag_lower("conexion")

    def _dibujar_nodo(self, nodo, x, y, separacion):
        if nodo is None:
            return

        canvas = self.canvas_arbol
        x_izquierdo = x - separacion
        x_derecho = x + separacion
        y_hijos = y + 95
        separacion_hijos = max(80, separacion // 2)

        if nodo.hijo_izquierdo is not None:
            canvas.create_line(x, y, x_izquierdo, y_hijos, fill="#818794", tags="conexion")
        if nodo.hijo_derecho is not None:
            canvas.create_line(x, y, x_derecho, y_hijos, fill="#818794", tags="conexion")

        self._dibujar_nodo(nodo.hijo_izquierdo, x_izquierdo, y_hijos, separacion_hijos)
        self._dibujar_nodo(nodo.hijo_derecho, x_derecho, y_hijos, separacion_hijos)

        if nodo.tipo == "Directorio":
            nombre = f"📁 {nodo.nombre}"
            fondo, borde, color_texto = "#DDEEFF", "#5286BC", "#173654"
        else:
            nombre = f"📄 {nodo.nombre}"
            if nodo.extension:
                nombre += f".{nodo.extension}"
            fondo, borde, color_texto = "#DCF4E2", "#438855", "#19482A"

        canvas.create_rectangle(
            x - 70, y - 22, x + 70, y + 22, fill=fondo, outline=borde
        )
        canvas.create_text(x, y, text=nombre, fill=color_texto, width=128)

    def _crear_dialogo(self, titulo, encabezado, color):
        dialogo = tk.Toplevel(self.ventana)
        dialogo.title(titulo)
        dialogo.transient(self.ventana)
        dialogo.resizable(False, False)

        tk.Label(
            dialogo, text=encabezado, bg=color, fg="white",
            font=("TkDefaultFont", 15, "bold"), padx=16, pady=12,
        ).pack(fill=tk.X)

        contenido = tk.Frame(dialogo, padx=18, pady=16)
        contenido.pack(fill=tk.BOTH, expand=True)
        dialogo.bind("<Escape>", lambda evento: dialogo.destroy())
        return dialogo, contenido

    def _activar_dialogo(self, dialogo, foco):
        dialogo.update_idletasks()
        dialogo.grab_set()
        foco.focus_force()

    def abrir_busqueda(self):
        self.dialogo_busqueda, contenido = self._crear_dialogo(
            "Buscar elemento", "🔍 Buscar elemento", "#603BA0"
        )
        tk.Label(contenido, text="Nombre del elemento").pack(anchor=tk.W)
        self.entrada_busqueda = tk.Entry(contenido, width=30)
        self.entrada_busqueda.pack(fill=tk.X, pady=(6, 14))

        botones = tk.Frame(contenido)
        botones.pack(anchor=tk.E)
        ttk.Button(
            botones, text="Aceptar", style="Insertar.TButton",
            command=self.confirmar_busqueda,
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            botones, text="Cancelar", style="Cancelar.TButton",
            command=self.dialogo_busqueda.destroy,
        ).pack(side=tk.LEFT)

        self.entrada_busqueda.bind("<Return>", self.confirmar_busqueda)
        self._activar_dialogo(self.dialogo_busqueda, self.entrada_busqueda)

    def confirmar_busqueda(self, evento=None):
        nombre = self.entrada_busqueda.get()
        self.dialogo_busqueda.destroy()
        nodo = self.sistema.buscar(nombre)
        if nodo is not None:
            self.mostrar_informacion(nodo)
        elif not nombre.strip():
            self.mostrar_error("Escribe el nombre del elemento.")
        else:
            self.mostrar_error("Elemento no encontrado.")

    def mostrar_informacion(self, nodo):
        titulo = "Información del elemento"
        dialogo, contenido = self._crear_dialogo(titulo, titulo, "#285C92")
        extension = nodo.extension or "Sin extensión"
        datos = (
            ("Nombre", nodo.nombre),
            ("Extensión", extension),
            ("Tipo", nodo.tipo),
            ("Tamaño", f"{nodo.tamano} bytes"),
        )
        for fila, (etiqueta, valor) in enumerate(datos):
            tk.Label(contenido, text=etiqueta).grid(row=fila, column=0, sticky=tk.W, pady=4)
            tk.Label(contenido, text=valor, wraplength=240, justify=tk.LEFT).grid(
                row=fila, column=1, sticky=tk.W, padx=(16, 0), pady=4
            )

        boton = ttk.Button(contenido, text="OK", style="Buscar.TButton", command=dialogo.destroy)
        boton.grid(row=4, column=0, columnspan=2, sticky=tk.E, pady=(12, 0))

        dialogo.bind("<Return>", lambda evento: dialogo.destroy())
        self._activar_dialogo(dialogo, boton)

    def mostrar_error(self, mensaje):
        titulo = "Error del sistema"
        dialogo, contenido = self._crear_dialogo(titulo, titulo, "#AD353E")
        tk.Label(contenido, text="✕", fg="#E35C65", font=("TkDefaultFont", 24, "bold")).pack()
        tk.Label(contenido, text=mensaje, wraplength=300, justify=tk.CENTER).pack(pady=(6, 14))

        boton = ttk.Button(
            contenido, text="Aceptar", style="Eliminar.TButton", command=dialogo.destroy
        )
        boton.pack()

        dialogo.bind("<Return>", lambda evento: dialogo.destroy())
        self._activar_dialogo(dialogo, boton)

    def abrir_eliminacion(self):
        self.dialogo_eliminacion, contenido = self._crear_dialogo(
            "Eliminar elemento", "Eliminar elemento", "#AD353E"
        )
        tk.Label(contenido, text="Nombre del elemento").pack(anchor=tk.W)
        self.entrada_eliminacion = tk.Entry(contenido, width=30)
        self.entrada_eliminacion.pack(fill=tk.X, pady=(6, 14))

        botones = tk.Frame(contenido)
        botones.pack(anchor=tk.E)
        ttk.Button(
            botones, text="Eliminar", style="Eliminar.TButton",
            command=self.confirmar_eliminacion,
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            botones, text="Cancelar", style="Cancelar.TButton",
            command=self.dialogo_eliminacion.destroy,
        ).pack(side=tk.LEFT)

        self.entrada_eliminacion.bind("<Return>", self.confirmar_eliminacion)
        self._activar_dialogo(self.dialogo_eliminacion, self.entrada_eliminacion)

    def confirmar_eliminacion(self, evento=None):
        nombre = self.entrada_eliminacion.get()
        self.dialogo_eliminacion.destroy()
        mensaje = self.sistema.eliminar(nombre)
        if mensaje.endswith("eliminado correctamente."):
            self.mostrar_mensaje(mensaje)
            self.dibujar_arbol()
        else:
            self.mostrar_error(mensaje)

    def abrir_despedida(self):
        if self.ventana.grab_current() is not None:
            return

        despedida = tk.Toplevel(self.ventana)
        despedida.title("Salir")
        despedida.transient(self.ventana)
        despedida.resizable(False, False)
        despedida.protocol("WM_DELETE_WINDOW", despedida.destroy)

        ancho, alto = 400, 330
        x = self.ventana.winfo_rootx() + (self.ventana.winfo_width() - ancho) // 2
        y = self.ventana.winfo_rooty() + (self.ventana.winfo_height() - alto) // 2
        despedida.geometry(f"{ancho}x{alto}+{x}+{y}")

        lila = "#F4EDFC"
        morado = "#603BA0"
        despedida.config(bg=lila)

        icono = tk.Canvas(despedida, width=80, height=80, bg=lila, highlightthickness=0)
        icono.pack(pady=(24, 12))
        icono.create_oval(4, 4, 76, 76, fill=morado, outline="")
        icono.create_text(40, 40, text="✓", fill="white", font=("TkDefaultFont", 30, "bold"))

        tk.Label(
            despedida, text="¡Hasta luego!", bg=lila, fg="#35204F",
            font=("TkDefaultFont", 24, "bold"),
        ).pack()
        tk.Label(despedida, text="Gracias por usar el", bg=lila, fg="#35204F").pack(pady=(8, 2))
        tk.Label(
            despedida, text="Sistema de Archivos", bg=lila, fg="#35204F",
            font=("TkDefaultFont", 14, "bold"),
        ).pack()

        botones = tk.Frame(despedida, bg=lila)
        botones.pack(pady=(22, 0))
        boton_volver = ttk.Button(
            botones, text="Volver", style="Cancelar.TButton", command=despedida.destroy
        )
        boton_volver.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(
            botones, text="Salir", style="Insertar.TButton", command=self.confirmar_salida
        ).pack(side=tk.LEFT)

        self._activar_dialogo(despedida, boton_volver)

    def confirmar_salida(self):
        self.ventana.destroy()

    def mostrar_mensaje(self, mensaje):
        self.resultados.config(state=tk.NORMAL)
        self.resultados.delete("1.0", tk.END)
        self.resultados.insert("1.0", mensaje)
        self.resultados.config(state=tk.DISABLED)


if __name__ == "__main__":
    ventana = tk.Tk()
    interfaz = InterfazSistemaArchivos(ventana)
    ventana.mainloop()
