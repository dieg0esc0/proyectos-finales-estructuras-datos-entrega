import tkinter as tk
from sistema_archivos import SistemaArchivos


class InterfazSistemaArchivos:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Archivos — Árbol Binario")
        self.ventana.geometry("750x500")
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

        self.resultados = tk.Text(contenido, wrap=tk.WORD)
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


if __name__ == "__main__":
    ventana = tk.Tk()
    interfaz = InterfazSistemaArchivos(ventana)
    ventana.mainloop()
