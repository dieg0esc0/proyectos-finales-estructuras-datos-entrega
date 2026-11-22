import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from navegador import Navegador, CAPACIDAD
from urls import normalizar_url, obtener_descripcion

MORADO = "#8b5cf6"
MORADO_CLARO = "#ede9fe"
VERDE = "#16a34a"
VERDE_CLARO = "#dcfce7"
AZUL = "#2563eb"
AZUL_CLARO = "#dbeafe"
ROJO = "#dc2626"
ROJO_CLARO = "#fee2e2"
FONDO = "#f8f7fc"
TEXTO = "#1f2937"


class VentanaNavegador:
    def __init__(self, ventana):
        self.ventana = ventana
        self.navegador = Navegador()
        self.ventana.title("Navegador Web (Pilas - LIFO)")
        self.ventana.geometry("900x720")
        self.ventana.minsize(820, 660)
        self.ventana.configure(bg=FONDO)
        self.ventana.protocol("WM_DELETE_WINDOW", self.salir)
        self.crear_estilos()
        self.crear_titulo()
        self.crear_barra_url()
        self.crear_botones()
        self.crear_panel_pagina()
        self.crear_panel_pilas()
        self.crear_registro()
        self.crear_barra_estado()
        self.actualizar_pantalla(False)
        self.mostrar_mensaje("¡Bienvenido! Escribe una URL y presiona Visitar (o Enter).", MORADO)
        self.entrada_url.focus_set()

    def crear_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Visitar.TButton", background=MORADO, foreground="white",
                         font=("Arial", 11, "bold"), padding=(18, 6), borderwidth=0)
        estilo.map("Visitar.TButton", background=[("active", "#7c3aed")])
        estilo.configure("Atras.TButton", background=VERDE_CLARO, foreground=VERDE,
                         font=("Arial", 11, "bold"), padding=(18, 6), bordercolor=VERDE)
        estilo.map("Atras.TButton", background=[("active", "#bbf7d0")])
        estilo.configure("Adelante.TButton", background=AZUL_CLARO, foreground=AZUL,
                         font=("Arial", 11, "bold"), padding=(18, 6), bordercolor=AZUL)
        estilo.map("Adelante.TButton", background=[("active", "#bfdbfe")])
        estilo.configure("Salir.TButton", background=ROJO_CLARO, foreground=ROJO,
                         font=("Arial", 11, "bold"), padding=(18, 6), bordercolor=ROJO)
        estilo.map("Salir.TButton", background=[("active", "#fecaca")])

    def crear_titulo(self):
        titulo = tk.Label(self.ventana, text="🌐  Navegador Web (Pilas - LIFO)",
                          font=("Arial", 18, "bold"), bg=MORADO, fg="white", pady=10)
        titulo.pack(fill="x")

    def crear_barra_url(self):
        marco = tk.Frame(self.ventana, bg=FONDO, pady=10, padx=20)
        marco.pack(fill="x")
        etiqueta = tk.Label(marco, text="URL:", font=("Arial", 12, "bold"), bg=FONDO, fg=MORADO)
        etiqueta.pack(side="left")
        self.entrada_url = tk.Entry(marco, font=("Arial", 12), relief="solid", bd=1,
                                    bg="white", fg=TEXTO, insertbackground=TEXTO,
                                    highlightthickness=1, highlightcolor=MORADO)
        self.entrada_url.pack(side="left", fill="x", expand=True, padx=10, ipady=5)
        self.entrada_url.bind("<Return>", self.visitar)
        boton_visitar = ttk.Button(marco, text="Visitar", style="Visitar.TButton",
                                   command=self.visitar)
        boton_visitar.pack(side="left")

    def crear_botones(self):
        marco = tk.Frame(self.ventana, bg=FONDO, padx=20)
        marco.pack(fill="x")
        boton_atras = ttk.Button(marco, text="←  Back", style="Atras.TButton",
                                 command=self.retroceder)
        boton_atras.pack(side="left", padx=(0, 10))
        boton_adelante = ttk.Button(marco, text="Forward  →", style="Adelante.TButton",
                                    command=self.avanzar)
        boton_adelante.pack(side="left", padx=(0, 10))
        boton_salir = ttk.Button(marco, text="⏻  Exit", style="Salir.TButton",
                                 command=self.salir)
        boton_salir.pack(side="left")

    def crear_panel_pagina(self):
        marco = tk.LabelFrame(self.ventana, text=" Página actual ", font=("Arial", 11, "bold"),
                              bg=MORADO_CLARO, fg=MORADO, padx=10, pady=10, relief="solid", bd=1)
        marco.pack(fill="x", padx=20, pady=12)
        self.etiqueta_icono = tk.Label(marco, text="🌐", font=("Arial", 40), bg=MORADO_CLARO, fg=MORADO)
        self.etiqueta_icono.pack(side="left", padx=(10, 20))
        textos = tk.Frame(marco, bg=MORADO_CLARO)
        textos.pack(side="left", fill="x", expand=True)
        self.etiqueta_pagina = tk.Label(textos, text="", font=("Arial", 17, "bold"),
                                        bg=MORADO_CLARO, fg=TEXTO, anchor="w")
        self.etiqueta_pagina.pack(fill="x")
        self.etiqueta_descripcion = tk.Label(textos, text="", font=("Arial", 12),
                                             bg=MORADO_CLARO, fg="#4b5563", anchor="w")
        self.etiqueta_descripcion.pack(fill="x", pady=(4, 0))

    def crear_panel_pilas(self):
        marco = tk.Frame(self.ventana, bg=FONDO)
        marco.pack(fill="x", padx=20)
        self.casillas_atras = []
        self.casillas_adelante = []
        panel_atras = self.crear_panel_una_pila(marco, "Pila atrás (Back stack)",
                                                VERDE, VERDE_CLARO, self.casillas_atras)
        panel_atras.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.etiqueta_cuenta_atras = panel_atras.etiqueta_cuenta
        self.etiqueta_aviso_atras = panel_atras.etiqueta_aviso
        panel_adelante = self.crear_panel_una_pila(marco, "Pila adelante (Forward stack)",
                                                   AZUL, AZUL_CLARO, self.casillas_adelante)
        panel_adelante.pack(side="left", fill="both", expand=True, padx=(8, 0))
        self.etiqueta_cuenta_adelante = panel_adelante.etiqueta_cuenta
        self.etiqueta_aviso_adelante = panel_adelante.etiqueta_aviso

    def crear_panel_una_pila(self, padre, titulo, color, color_claro, casillas):
        panel = tk.LabelFrame(padre, text=" ☰ " + titulo + " ", font=("Arial", 11, "bold"),
                              bg="white", fg=color, padx=10, pady=8, relief="solid", bd=1)
        posicion = CAPACIDAD
        while posicion >= 1:
            fila = tk.Frame(panel, bg="white")
            fila.pack(fill="x", pady=2)
            numero = tk.Label(fila, text=str(posicion), width=3, font=("Arial", 10, "bold"),
                              bg=color_claro, fg=color, relief="solid", bd=1)
            numero.pack(side="left")
            casilla = tk.Label(fila, text="", font=("Arial", 10), bg="white", fg=TEXTO,
                               anchor="w", relief="solid", bd=1, padx=6, pady=3,
                               highlightbackground=color)
            casilla.pack(side="left", fill="x", expand=True, padx=(4, 0))
            casillas.append(casilla)
            posicion = posicion - 1
        panel.etiqueta_cuenta = tk.Label(panel, text="", font=("Arial", 10), bg="white", fg="#6b7280")
        panel.etiqueta_cuenta.pack(anchor="w", pady=(6, 0))
        panel.etiqueta_aviso = tk.Label(panel, text="", font=("Arial", 12, "bold"),
                                        bg="white", fg=ROJO)
        panel.etiqueta_aviso.pack(fill="x")
        return panel

    def crear_registro(self):
        marco = tk.LabelFrame(self.ventana, text=" Registro de operaciones (push / pop) ",
                              font=("Arial", 11, "bold"), bg="white", fg="#4b5563",
                              padx=8, pady=6, relief="solid", bd=1)
        marco.pack(fill="both", expand=True, padx=20, pady=12)
        barra = tk.Scrollbar(marco)
        barra.pack(side="right", fill="y")
        self.lista_registro = tk.Listbox(marco, font=("Courier", 10), height=6, bd=0,
                                         bg="white", fg=TEXTO, selectbackground=MORADO_CLARO,
                                         selectforeground=TEXTO, highlightthickness=0,
                                         yscrollcommand=barra.set)
        self.lista_registro.pack(side="left", fill="both", expand=True)
        barra.config(command=self.lista_registro.yview)

    def crear_barra_estado(self):
        self.etiqueta_estado = tk.Label(self.ventana, text="", font=("Arial", 11, "bold"),
                                        bg="white", anchor="w", padx=20, pady=8,
                                        relief="solid", bd=1)
        self.etiqueta_estado.pack(fill="x", side="bottom")

    def mostrar_mensaje(self, texto, color):
        self.etiqueta_estado.config(text=texto, fg=color)

    def limpiar_avisos(self):
        self.etiqueta_aviso_atras.config(text="")
        self.etiqueta_aviso_adelante.config(text="")

    def dibujar_pila(self, pila, casillas, etiqueta_cuenta, color_claro):
        elementos = pila.obtener_elementos()
        indice = 0
        while indice < len(casillas):
            posicion = CAPACIDAD - indice
            casilla = casillas[indice]
            if posicion <= pila.tamano:
                url = elementos[pila.tamano - posicion]
                if posicion == pila.tamano:
                    casilla.config(text=url + "    ◄ tope", bg=color_claro,
                                   font=("Arial", 10, "bold"))
                else:
                    casilla.config(text=url, bg=color_claro, font=("Arial", 10))
            else:
                casilla.config(text="", bg="white", font=("Arial", 10))
            indice = indice + 1
        etiqueta_cuenta.config(text="Elementos: " + str(pila.tamano) + " / " + str(CAPACIDAD))

    def actualizar_pantalla(self, cambiar_url):
        actual = self.navegador.pagina_actual
        if actual is None:
            self.etiqueta_pagina.config(text="Ninguna página abierta")
            self.etiqueta_descripcion.config(text="La página actual se mostrará aquí")
            self.ventana.title("Navegador Web (Pilas - LIFO)")
        else:
            self.etiqueta_pagina.config(text=actual)
            self.etiqueta_descripcion.config(text=obtener_descripcion(actual))
            self.ventana.title("Navegador Web (Pilas - LIFO)  -  " + actual)
            if cambiar_url:
                self.entrada_url.delete(0, tk.END)
                self.entrada_url.insert(0, actual)
        self.dibujar_pila(self.navegador.pila_atras, self.casillas_atras,
                          self.etiqueta_cuenta_atras, VERDE_CLARO)
        self.dibujar_pila(self.navegador.pila_adelante, self.casillas_adelante,
                          self.etiqueta_cuenta_adelante, AZUL_CLARO)
        self.lista_registro.delete(0, tk.END)
        for linea in self.navegador.registro:
            self.lista_registro.insert(tk.END, linea)
        self.lista_registro.see(tk.END)

    def visitar(self, evento=None):
        texto = self.entrada_url.get().strip()
        self.limpiar_avisos()
        if texto == "":
            self.mostrar_mensaje("Escribe una URL antes de presionar Visitar.", ROJO)
            messagebox.showwarning("URL vacía", "Por favor escribe una URL para visitar.\n"
                                   "Ejemplo: https://www.google.com")
            return
        url = normalizar_url(texto)
        if url is None:
            self.mostrar_mensaje("La URL \"" + texto + "\" no es válida.", ROJO)
            messagebox.showwarning("URL no válida", "La URL \"" + texto + "\" no es válida.\n"
                                   "Ejemplo de URL correcta: https://www.google.com")
            return
        resultado = self.navegador.visitar(url)
        if resultado == "MISMA":
            self.mostrar_mensaje("Ya te encuentras en " + self.navegador.pagina_actual, AZUL)
        elif resultado == "LLENA":
            self.etiqueta_aviso_atras.config(text="✗  PILA LLENA")
            self.mostrar_mensaje("Pila atrás llena: no se pudo visitar " + url, ROJO)
            messagebox.showwarning("Pila llena",
                                   "La pila atrás está llena (máximo " + str(CAPACIDAD) +
                                   " páginas).\nNo se puede guardar más historial.\n"
                                   "Usa Back para liberar espacio.")
        else:
            self.mostrar_mensaje("✔  Visitaste " + url, VERDE)
        self.actualizar_pantalla(resultado == "OK")

    def retroceder(self):
        self.limpiar_avisos()
        resultado = self.navegador.retroceder()
        if resultado == "VACIA":
            self.etiqueta_aviso_atras.config(text="✗  PILA VACÍA")
            self.mostrar_mensaje("No hay páginas anteriores para regresar.", ROJO)
            messagebox.showinfo("Pila vacía", "No hay páginas anteriores.\n"
                                "La pila atrás está vacía.")
        elif resultado == "LLENA":
            self.etiqueta_aviso_adelante.config(text="✗  PILA LLENA")
            self.mostrar_mensaje("La pila adelante está llena.", ROJO)
        else:
            self.mostrar_mensaje("←  Regresaste a " + self.navegador.pagina_actual, VERDE)
        self.actualizar_pantalla(resultado == "OK")

    def avanzar(self):
        self.limpiar_avisos()
        resultado = self.navegador.avanzar()
        if resultado == "VACIA":
            self.etiqueta_aviso_adelante.config(text="✗  PILA VACÍA")
            self.mostrar_mensaje("No hay páginas siguientes para avanzar.", ROJO)
            messagebox.showinfo("Pila vacía", "No hay páginas siguientes.\n"
                                "La pila adelante está vacía.")
        elif resultado == "LLENA":
            self.etiqueta_aviso_atras.config(text="✗  PILA LLENA")
            self.mostrar_mensaje("La pila atrás está llena.", ROJO)
        else:
            self.mostrar_mensaje("→  Avanzaste a " + self.navegador.pagina_actual, AZUL)
        self.actualizar_pantalla(resultado == "OK")

    def salir(self):
        respuesta = messagebox.askyesno("Salir", "¿Seguro que deseas salir del navegador?")
        if respuesta:
            self.ventana.destroy()
