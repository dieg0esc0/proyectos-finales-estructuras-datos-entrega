import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import time

CAPACIDAD = 6

COMPUTADORAS = ["PC1", "PC2", "PC3", "PC4", "PC5"]

DOCUMENTOS = ["Tarea.docx", "Reporte.pdf", "Examen.pdf", "Presentacion.pptx",
              "Calificaciones.xlsx", "Proyecto.docx", "Foto.png", "Factura.pdf"]

AZUL = "#1d4ed8"
AZUL_CLARO = "#dbeafe"
AMARILLO = "#fde68a"
VERDE = "#16a34a"
VERDE_CLARO = "#dcfce7"
ROJO = "#dc2626"
ROJO_CLARO = "#fee2e2"
NARANJA = "#f59e0b"
FONDO = "#f5f7fb"
TEXTO = "#1f2937"
GRIS = "#6b7280"


class Trabajo:
    def __init__(self, numero, computadora, documento):
        self.numero = numero
        self.computadora = computadora
        self.documento = documento
        self.hora = time.strftime("%H:%M:%S")

    def texto_corto(self):
        return self.computadora + " - " + self.documento

    def texto_largo(self):
        return "#" + str(self.numero) + "  " + self.computadora + "  " + self.documento + "  (" + self.hora + ")"


class Cola:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.datos = []
        contador = 0
        while contador < capacidad:
            self.datos.append(None)
            contador = contador + 1
        self.frente = 0
        self.final = -1
        self.tamano = 0

    def esta_vacia(self):
        return self.tamano == 0

    def esta_llena(self):
        return self.tamano == self.capacidad

    def encolar(self, dato):
        if self.esta_llena():
            return False
        self.final = (self.final + 1) % self.capacidad
        self.datos[self.final] = dato
        self.tamano = self.tamano + 1
        return True

    def desencolar(self):
        if self.esta_vacia():
            return None
        dato = self.datos[self.frente]
        self.datos[self.frente] = None
        self.frente = (self.frente + 1) % self.capacidad
        self.tamano = self.tamano - 1
        return dato

    def ver_frente(self):
        if self.esta_vacia():
            return None
        return self.datos[self.frente]

    def obtener_elementos(self):
        elementos = []
        posicion = self.frente
        contador = 0
        while contador < self.tamano:
            elementos.append(self.datos[posicion])
            posicion = (posicion + 1) % self.capacidad
            contador = contador + 1
        return elementos


class ColaImpresion:
    def __init__(self):
        self.cola = Cola(CAPACIDAD)
        self.siguiente_numero = 1
        self.impresos = []
        self.registro = []

    def elegir_computadora(self):
        indice = random.randint(0, len(COMPUTADORAS) - 1)
        return COMPUTADORAS[indice]

    def elegir_documento(self):
        indice = random.randint(0, len(DOCUMENTOS) - 1)
        return DOCUMENTOS[indice]

    def agregar_trabajo(self, computadora):
        if self.cola.esta_llena():
            self.registro.append("ENCOLAR " + computadora + "  ->  rechazado, cola LLENA")
            return None
        trabajo = Trabajo(self.siguiente_numero, computadora, self.elegir_documento())
        self.cola.encolar(trabajo)
        self.siguiente_numero = self.siguiente_numero + 1
        self.registro.append("ENCOLAR  " + trabajo.texto_largo())
        return trabajo

    def imprimir(self):
        if self.cola.esta_vacia():
            self.registro.append("DESENCOLAR  ->  cola VACÍA, nada que imprimir")
            return None
        trabajo = self.cola.desencolar()
        self.impresos.append(trabajo)
        self.registro.append("DESENCOLAR  " + trabajo.texto_largo())
        return trabajo


class BotonComputadora:
    def __init__(self, padre, aplicacion, nombre):
        self.aplicacion = aplicacion
        self.nombre = nombre
        self.boton = tk.Button(padre, text="💻 " + nombre, font=("Arial", 10, "bold"), width=8,
                               bg="white", fg=AZUL, relief="solid", bd=1, command=self.enviar)
        self.boton.pack(pady=3)

    def enviar(self):
        self.aplicacion.agregar_trabajo(self.nombre)

    def resaltar(self, activo):
        if activo:
            self.boton.config(bg=AMARILLO, highlightbackground=AMARILLO)
        else:
            self.boton.config(bg="white", highlightbackground="white")


class VentanaCola:
    def __init__(self, ventana):
        self.ventana = ventana
        self.sistema = ColaImpresion()
        self.ultimo_agregado = False
        self.ventana.title("Cola de impresión (FIFO)")
        self.ventana.geometry("980x720")
        self.ventana.minsize(920, 680)
        self.ventana.configure(bg=FONDO)
        self.ventana.protocol("WM_DELETE_WINDOW", self.salir)
        self.crear_estilos()
        self.crear_titulo()
        self.crear_zona_principal()
        self.crear_listas()
        self.crear_barra_estado()
        self.actualizar_pantalla()
        self.mostrar_estado("¡Bienvenido! Presiona \"Agregar trabajo\" para que una PC al azar mande a imprimir.", AZUL)

    def crear_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Imprimir.TButton", background=VERDE, foreground="white",
                         font=("Arial", 12, "bold"), padding=(16, 8), borderwidth=0)
        estilo.map("Imprimir.TButton", background=[("active", "#15803d")])
        estilo.configure("Agregar.TButton", background=AZUL, foreground="white",
                         font=("Arial", 11, "bold"), padding=(10, 6), borderwidth=0)
        estilo.map("Agregar.TButton", background=[("active", "#1e40af")])
        estilo.configure("Mostrar.TButton", background=AZUL_CLARO, foreground=AZUL,
                         font=("Arial", 11, "bold"), padding=(10, 6), bordercolor=AZUL)
        estilo.map("Mostrar.TButton", background=[("active", "#bfdbfe")])
        estilo.configure("Salir.TButton", background=ROJO_CLARO, foreground=ROJO,
                         font=("Arial", 11, "bold"), padding=(10, 6), bordercolor=ROJO)
        estilo.map("Salir.TButton", background=[("active", "#fecaca")])

    def crear_titulo(self):
        titulo = tk.Label(self.ventana, text="🖨  PROYECTO COLA DE IMPRESIÓN  (FIFO)",
                          font=("Arial", 18, "bold"), bg=AZUL, fg="white", pady=10)
        titulo.pack(fill="x")
        subtitulo = tk.Label(self.ventana, text="Las computadoras envían trabajos a la cola. "
                             "Los trabajos se atienden en orden de llegada: el primero que entra es el primero en imprimirse.",
                             font=("Arial", 10), bg=FONDO, fg=GRIS, pady=6)
        subtitulo.pack(fill="x")

    def crear_zona_principal(self):
        marco = tk.LabelFrame(self.ventana, text=" Cola de impresión ", font=("Arial", 12, "bold"),
                              bg="white", fg=AZUL, padx=12, pady=10, relief="solid", bd=1)
        marco.pack(fill="x", padx=20, pady=(4, 10))
        columna_pcs = tk.Frame(marco, bg="white")
        columna_pcs.pack(side="left", padx=(0, 14))
        tk.Label(columna_pcs, text="Computadoras", font=("Arial", 9, "bold"), bg="white", fg=GRIS).pack()
        self.botones_pc = []
        for nombre in COMPUTADORAS:
            self.botones_pc.append(BotonComputadora(columna_pcs, self, nombre))
        centro = tk.Frame(marco, bg="white")
        centro.pack(side="left", fill="both", expand=True)
        self.crear_casillas(centro)
        self.etiqueta_arreglo = tk.Label(centro, text="", font=("Courier", 10), bg="white", fg=GRIS, anchor="w")
        self.etiqueta_arreglo.pack(fill="x", pady=(6, 0))
        self.etiqueta_mensaje = tk.Label(centro, text="", font=("Arial", 14, "bold"), bg="white",
                                         fg=TEXTO, relief="solid", bd=1, highlightthickness=0,
                                         pady=12)
        self.etiqueta_mensaje.pack(fill="x", pady=(10, 0))
        self.etiqueta_cuenta = tk.Label(centro, text="", font=("Arial", 10), bg="white", fg=GRIS, anchor="w")
        self.etiqueta_cuenta.pack(fill="x", pady=(6, 0))
        derecha = tk.Frame(marco, bg="white")
        derecha.pack(side="left", padx=(14, 0), fill="y")
        ttk.Button(derecha, text="Imprimir", style="Imprimir.TButton",
                   command=self.imprimir).pack(fill="x")
        self.etiqueta_impresora = tk.Label(derecha, text="🖨", font=("Arial", 54), bg="white", fg=AZUL)
        self.etiqueta_impresora.pack(pady=2)
        self.etiqueta_imprimiendo = tk.Label(derecha, text="", font=("Arial", 9), bg="white",
                                             fg=GRIS, wraplength=170)
        self.etiqueta_imprimiendo.pack()
        ttk.Button(derecha, text="➕ Agregar trabajo", style="Agregar.TButton",
                   command=self.agregar_aleatorio).pack(fill="x", pady=(8, 4))
        ttk.Button(derecha, text="☰ Mostrar cola", style="Mostrar.TButton",
                   command=self.mostrar_cola).pack(fill="x", pady=4)
        ttk.Button(derecha, text="⏻ Salir", style="Salir.TButton",
                   command=self.salir).pack(fill="x", pady=4)

    def crear_casillas(self, padre):
        fila_casillas = tk.Frame(padre, bg="white")
        fila_casillas.pack(fill="x")
        self.casillas = []
        self.marcas = []
        posicion = 0
        while posicion < CAPACIDAD:
            columna = tk.Frame(fila_casillas, bg="white")
            columna.pack(side="left", padx=3, expand=True, fill="x")
            casilla = tk.Label(columna, text="", font=("Arial", 10, "bold"), width=9, height=4,
                               bg="white", fg=TEXTO, relief="solid", bd=1)
            casilla.pack(fill="x")
            marca = tk.Label(columna, text="", font=("Arial", 9, "bold"), bg="white", fg=AZUL)
            marca.pack()
            self.casillas.append(casilla)
            self.marcas.append(marca)
            posicion = posicion + 1

    def crear_listas(self):
        marco = tk.Frame(self.ventana, bg=FONDO)
        marco.pack(fill="both", expand=True, padx=20)
        self.lista_impresos = self.crear_una_lista(marco, " ✔ Trabajos impresos ", VERDE)
        self.lista_registro = self.crear_una_lista(marco, " Registro de operaciones (encolar / desencolar) ", GRIS)

    def crear_una_lista(self, padre, titulo, color):
        marco = tk.LabelFrame(padre, text=titulo, font=("Arial", 11, "bold"), bg="white", fg=color,
                              padx=8, pady=6, relief="solid", bd=1)
        marco.pack(side="left", fill="both", expand=True, padx=4, pady=(0, 10))
        barra = tk.Scrollbar(marco)
        barra.pack(side="right", fill="y")
        lista = tk.Listbox(marco, font=("Courier", 10), height=8, bd=0, highlightthickness=0,
                           bg="white", fg=TEXTO, selectbackground=AZUL_CLARO,
                           selectforeground=TEXTO, yscrollcommand=barra.set)
        lista.pack(side="left", fill="both", expand=True)
        barra.config(command=lista.yview)
        return lista

    def crear_barra_estado(self):
        self.etiqueta_estado = tk.Label(self.ventana, text="", font=("Arial", 11, "bold"), bg="white",
                                        anchor="w", padx=20, pady=8, relief="solid", bd=1)
        self.etiqueta_estado.pack(fill="x", side="bottom")

    def mostrar_estado(self, texto, color):
        self.etiqueta_estado.config(text=texto, fg=color)

    def mostrar_mensaje(self, texto, color, fondo):
        self.etiqueta_mensaje.config(text=texto, fg=color, bg=fondo)

    def resaltar_computadora(self, nombre):
        for boton in self.botones_pc:
            boton.resaltar(boton.nombre == nombre)

    def dibujar_cola(self):
        elementos = self.sistema.cola.obtener_elementos()
        tamano = len(elementos)
        posicion = 0
        while posicion < CAPACIDAD:
            casilla = self.casillas[posicion]
            marca = self.marcas[posicion]
            if posicion < tamano:
                trabajo = elementos[posicion]
                texto = "📄\n" + trabajo.computadora + "\n#" + str(trabajo.numero)
                color = AZUL_CLARO
                if self.ultimo_agregado and posicion == tamano - 1:
                    color = AMARILLO
                casilla.config(text=texto, bg=color)
            else:
                casilla.config(text="", bg="white")
            marca.config(text="")
            posicion = posicion + 1
        if tamano == 1:
            self.marcas[0].config(text="▲ frente / final")
        elif tamano > 1:
            self.marcas[0].config(text="▲ frente")
            self.marcas[tamano - 1].config(text="▲ final")

    def dibujar_arreglo(self):
        cola = self.sistema.cola
        texto = "Arreglo interno: ["
        indice = 0
        while indice < cola.capacidad:
            if cola.datos[indice] is None:
                texto = texto + " -- "
            else:
                texto = texto + " " + cola.datos[indice].computadora + " "
            if indice < cola.capacidad - 1:
                texto = texto + "|"
            indice = indice + 1
        texto = texto + "]   frente = " + str(cola.frente) + "   final = " + str(cola.final)
        self.etiqueta_arreglo.config(text=texto)

    def actualizar_pantalla(self):
        self.dibujar_cola()
        self.dibujar_arreglo()
        cola = self.sistema.cola
        self.etiqueta_cuenta.config(text="Trabajos en cola: " + str(cola.tamano) + " / " + str(CAPACIDAD) +
                                    "      Trabajos impresos: " + str(len(self.sistema.impresos)))
        self.lista_impresos.delete(0, tk.END)
        for trabajo in self.sistema.impresos:
            self.lista_impresos.insert(tk.END, trabajo.texto_largo())
        self.lista_impresos.see(tk.END)
        self.lista_registro.delete(0, tk.END)
        for linea in self.sistema.registro:
            self.lista_registro.insert(tk.END, linea)
        self.lista_registro.see(tk.END)

    def agregar_aleatorio(self):
        computadora = self.sistema.elegir_computadora()
        self.agregar_trabajo(computadora)

    def agregar_trabajo(self, computadora):
        self.resaltar_computadora(computadora)
        trabajo = self.sistema.agregar_trabajo(computadora)
        if trabajo is None:
            self.ultimo_agregado = False
            self.mostrar_mensaje("✗  La cola de impresión está LLENA", ROJO, ROJO_CLARO)
            self.mostrar_estado(computadora + " no pudo enviar su trabajo porque la cola está llena. "
                                "Presiona Imprimir para liberar espacio.", ROJO)
            self.actualizar_pantalla()
            messagebox.showwarning("Cola llena", "La cola de impresión está LLENA\n\n"
                                   "Capacidad máxima: " + str(CAPACIDAD) + " trabajos.")
            return
        self.ultimo_agregado = True
        self.mostrar_mensaje("", TEXTO, "white")
        self.mostrar_estado("✔  " + computadora + " envió \"" + trabajo.documento +
                            "\" (trabajo #" + str(trabajo.numero) + ") al final de la cola.", VERDE)
        self.actualizar_pantalla()

    def imprimir(self):
        self.ultimo_agregado = False
        self.resaltar_computadora("")
        trabajo = self.sistema.imprimir()
        if trabajo is None:
            self.etiqueta_imprimiendo.config(text="")
            self.mostrar_mensaje("✗  La cola de impresión está VACÍA", ROJO, ROJO_CLARO)
            self.mostrar_estado("No hay trabajos pendientes para imprimir.", ROJO)
            self.actualizar_pantalla()
            messagebox.showinfo("Cola vacía", "La cola de impresión está VACÍA\n\n"
                                "No hay trabajos pendientes.")
            return
        self.mostrar_mensaje("Impresión " + trabajo.computadora, TEXTO, "#fff7ed")
        self.etiqueta_imprimiendo.config(text="Atendiendo a " + trabajo.computadora + ":\n" + trabajo.documento)
        self.mostrar_estado("🖨  Se está atendiendo a " + trabajo.computadora + " (trabajo #" +
                            str(trabajo.numero) + ", " + trabajo.documento + "). Los demás trabajos avanzan.", AZUL)
        self.actualizar_pantalla()

    def mostrar_cola(self):
        elementos = self.sistema.cola.obtener_elementos()
        if len(elementos) == 0:
            messagebox.showinfo("Cola de impresión", "La cola de impresión está VACÍA\n\n"
                                "No hay trabajos pendientes.")
            return
        texto = "Trabajos pendientes en orden de atención:\n\n"
        lugar = 1
        for trabajo in elementos:
            texto = texto + str(lugar) + ".  " + trabajo.texto_corto() + "   (#" + str(trabajo.numero) + ")\n"
            lugar = lugar + 1
        texto = texto + "\nTotal: " + str(len(elementos)) + " de " + str(CAPACIDAD) + " lugares ocupados."
        messagebox.showinfo("Cola de impresión", texto)
        self.mostrar_estado("Se mostró la cola: " + str(len(elementos)) + " trabajo(s) pendiente(s).", AZUL)

    def salir(self):
        respuesta = messagebox.askyesno("Salir", "¿Seguro que deseas salir de la cola de impresión?")
        if respuesta:
            self.ventana.destroy()


ventana_principal = tk.Tk()
aplicacion = VentanaCola(ventana_principal)
ventana_principal.mainloop()
