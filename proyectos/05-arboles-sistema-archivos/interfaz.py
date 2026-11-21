import tkinter as tk
from sistema_archivos import SistemaArchivos


class InterfazSistemaArchivos:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Archivos — Árbol Binario")
        self.ventana.geometry("750x650")
        self.sistema = SistemaArchivos("Documentos")

        contenido = tk.Frame(self.ventana, padx=20, pady=20)
        contenido.pack(fill=tk.BOTH, expand=True)

        titulo = tk.Label(
            contenido,
            text="Sistema de Archivos — Árbol Binario",
            font=("TkDefaultFont", 18, "bold"),
        )
        titulo.pack(anchor=tk.W)

        descripcion = tk.Label(contenido, text="Directorio raíz: Documentos")
        descripcion.pack(anchor=tk.W, pady=(6, 14))

        boton_raiz = tk.Button(contenido, text="Mostrar raíz", command=self.mostrar_raiz)
        boton_raiz.pack(anchor=tk.W)


        formulario_directorio = tk.Frame(contenido)
        formulario_directorio.pack(fill=tk.X, pady=(12, 0))
        tk.Label(formulario_directorio, text="Crear directorio").grid(
            row=0, column=0, columnspan=3, sticky=tk.W
        )
        tk.Label(formulario_directorio, text="Nombre").grid(row=1, column=0, sticky=tk.W)
        self.entrada_directorio = tk.Entry(formulario_directorio)
        self.entrada_directorio.grid(row=1, column=1, padx=8, pady=4)
        tk.Button(
            formulario_directorio, text="Crear directorio", command=self.crear_directorio
        ).grid(row=1, column=2, sticky=tk.W)

        formulario_archivo = tk.Frame(contenido)
        formulario_archivo.pack(fill=tk.X, pady=(12, 0))
        tk.Label(formulario_archivo, text="Insertar archivo").grid(
            row=0, column=0, columnspan=3, sticky=tk.W
        )
        tk.Label(formulario_archivo, text="Nombre").grid(row=1, column=0, sticky=tk.W)
        self.entrada_nombre_archivo = tk.Entry(formulario_archivo)
        self.entrada_nombre_archivo.grid(row=1, column=1, padx=8, pady=4)

        tk.Label(formulario_archivo, text="Extensión").grid(row=2, column=0, sticky=tk.W)
        self.entrada_extension = tk.Entry(formulario_archivo)
        self.entrada_extension.grid(row=2, column=1, padx=8, pady=4)

        tk.Label(formulario_archivo, text="Tamaño").grid(row=3, column=0, sticky=tk.W)
        self.entrada_tamano = tk.Entry(formulario_archivo)
        self.entrada_tamano.grid(row=3, column=1, padx=8, pady=4)
        tk.Button(
            formulario_archivo, text="Insertar archivo", command=self.insertar_archivo
        ).grid(row=3, column=2, sticky=tk.W)

        self.resultados = tk.Text(contenido, wrap=tk.WORD, height=8)
        self.resultados.pack(fill=tk.BOTH, expand=True, pady=12)
        self.resultados.config(state=tk.DISABLED)

        boton_salir = tk.Button(contenido, text="Salir", command=self.ventana.destroy)
        boton_salir.pack(anchor=tk.E)

    def mostrar_mensaje(self, mensaje):
        self.resultados.config(state=tk.NORMAL)
        self.resultados.delete("1.0", tk.END)
        self.resultados.insert("1.0", mensaje)
        self.resultados.config(state=tk.DISABLED)

    def mostrar_raiz(self):
        mensaje = self.sistema.mostrar_raiz()
        self.mostrar_mensaje(mensaje)


    def crear_directorio(self):
        nombre = self.entrada_directorio.get()
        mensaje = self.sistema.insertar_directorio(nombre)
        self.mostrar_mensaje(mensaje)

        if mensaje.endswith("insertado correctamente."):
            self.entrada_directorio.delete(0, tk.END)

    def insertar_archivo(self):
        nombre = self.entrada_nombre_archivo.get()
        extension = self.entrada_extension.get()
        entrada_tamano = self.entrada_tamano.get()

        try:
            tamano = int(entrada_tamano)
        except ValueError:
            self.mostrar_mensaje("El tamaño debe ser un número entero.")
            return

        mensaje = self.sistema.insertar_archivo(nombre, extension, tamano)
        self.mostrar_mensaje(mensaje)

        if mensaje.endswith("insertado correctamente."):
            self.entrada_nombre_archivo.delete(0, tk.END)
            self.entrada_extension.delete(0, tk.END)
            self.entrada_tamano.delete(0, tk.END)


if __name__ == "__main__":
    ventana = tk.Tk()
    interfaz = InterfazSistemaArchivos(ventana)
    ventana.mainloop()
