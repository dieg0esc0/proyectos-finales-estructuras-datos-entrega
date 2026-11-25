# Proyecto de Listas - Carrito de compras
# Versión gráfica del programa hecha con Tkinter.
# Usa las mismas clases Catalogo y Carrito (listas enlazadas) que la versión de consola.

import tkinter as tk
from tkinter import messagebox
from carrito import Catalogo, Carrito

AZUL = "#1F6FD1"
VERDE = "#2E9E5B"
FUENTE_LISTA = ("Courier", 13)


def obtener_en_posicion(lista, posicion):
    # Recorre la lista enlazada desde el primer nodo y regresa el dato
    # que está en esa posición (0 es el primero). Si no existe regresa None.
    actual = lista.primerNodo
    contador = 0
    while actual is not None:
        if contador == posicion:
            return actual.datos
        contador = contador + 1
        actual = actual.siguienteNodo
    return None


class VentanaCarrito:
    # Ventana del programa: a la izquierda el catálogo y a la derecha el carrito.

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Proyecto Listas - Carrito de compras")
        self.catalogo = Catalogo()
        self.carrito = Carrito()

        titulo = tk.Label(raiz, text="CARRITO DE COMPRAS", font=("Arial", 22, "bold"), fg=AZUL)
        titulo.pack(pady=10)

        contenedor = tk.Frame(raiz)
        contenedor.pack(padx=10, pady=5)
        self.crear_panel_catalogo(contenedor)
        self.crear_panel_carrito(contenedor)

        self.mostrar_catalogo()
        self.actualizar_carrito()

    # ------------------------- Catálogo (R1, R2 y R3) -------------------------

    def crear_panel_catalogo(self, contenedor):
        # Crea la búsqueda, la lista de productos, la cantidad y el botón de agregar.
        panel = tk.LabelFrame(contenedor, text="Catálogo de productos", font=("Arial", 13, "bold"))
        panel.pack(side="left", padx=8, anchor="n")

        fila = tk.Frame(panel)
        fila.pack(pady=6)
        tk.Label(fila, text="Buscar (ID o nombre):").pack(side="left")
        self.entrada_buscar = tk.Entry(fila, width=16)
        self.entrada_buscar.pack(side="left", padx=4)
        tk.Button(fila, text="Buscar", command=self.buscar).pack(side="left")

        tk.Label(panel, text="ID   Producto          Precio", font=FUENTE_LISTA, anchor="w").pack(fill="x", padx=8)
        self.lista_catalogo = tk.Listbox(panel, width=32, height=12, font=FUENTE_LISTA, exportselection=False)
        self.lista_catalogo.pack(padx=8, fill="x")

        fila2 = tk.Frame(panel)
        fila2.pack(pady=8)
        tk.Label(fila2, text="Cantidad:").pack(side="left")
        self.cantidad = tk.Spinbox(fila2, from_=1, to=100, width=5)
        self.cantidad.pack(side="left", padx=4)
        tk.Button(fila2, text="Agregar al carrito →", fg=AZUL, command=self.agregar).pack(side="left", padx=4)

        self.mensaje = tk.Label(panel, text="Selecciona un producto y presiona Agregar.", fg="gray")
        self.mensaje.pack(pady=(0, 8))

    def mostrar_catalogo(self):
        # R1: recorre la lista del catálogo y pone un renglón por producto.
        self.lista_catalogo.delete(0, "end")
        actual = self.catalogo.productos.primerNodo
        while actual is not None:
            p = actual.datos
            renglon = str(p.id).ljust(5) + p.nombre.ljust(18) + "$" + str(p.precio)
            self.lista_catalogo.insert("end", renglon)
            actual = actual.siguienteNodo

    def buscar(self):
        # R2: busca por ID si se escribe un número, o por nombre si se escribe texto.
        texto = self.entrada_buscar.get().strip()
        if texto == "":
            self.avisar("Escribe un ID o un nombre para buscar.", "red")
            return
        # isdecimal() solo acepta dígitos que int() sí puede convertir (isdigit() también acepta ²).
        if texto.isdecimal():
            producto = self.catalogo.buscar_por_id(int(texto))
        else:
            producto = self.catalogo.buscar_por_nombre(texto)
        if producto is None:
            self.avisar("No se encontró el producto.", "red")
            return

        # Recorre el catálogo para saber en qué renglón está y lo selecciona.
        posicion = 0
        actual = self.catalogo.productos.primerNodo
        while actual.datos != producto:
            posicion = posicion + 1
            actual = actual.siguienteNodo
        self.lista_catalogo.selection_clear(0, "end")
        self.lista_catalogo.selection_set(posicion)
        self.lista_catalogo.see(posicion)
        self.avisar("Encontrado: " + producto.nombre + " ($" + str(producto.precio) + ")", "black")

    def leer_cantidad(self, caja):
        # Lee la cantidad de una caja y revisa que sea un entero de 1 a 100.
        try:
            cantidad = int(caja.get())
        except ValueError:
            return None
        if cantidad < 1 or cantidad > 100:
            return None
        return cantidad

    def agregar(self):
        # R3: agrega el producto seleccionado con la cantidad elegida.
        seleccion = self.lista_catalogo.curselection()
        if len(seleccion) == 0:
            self.avisar("Primero selecciona un producto del catálogo.", "red")
            return
        cantidad = self.leer_cantidad(self.cantidad)
        if cantidad is None:
            self.avisar("La cantidad debe ser un número entero de 1 a 100.", "red")
            return
        producto = obtener_en_posicion(self.catalogo.productos, seleccion[0])
        self.carrito.agregar(producto, cantidad)
        self.actualizar_carrito()
        self.avisar("Se agregó " + producto.nombre + " al carrito.", VERDE)

    def avisar(self, texto, color):
        self.mensaje.config(text=texto, fg=color)

    # ------------------------- Carrito (R4 a R8) -------------------------

    def crear_panel_carrito(self, contenedor):
        # Crea la lista del carrito, los botones para cambiarlo, los totales y Finalizar.
        panel = tk.LabelFrame(contenedor, text="Mi carrito", font=("Arial", 13, "bold"))
        panel.pack(side="left", padx=8, anchor="n")

        tk.Label(panel, text="ID   Producto      Cant  Subtotal", font=FUENTE_LISTA, anchor="w").pack(fill="x", padx=8, pady=(6, 0))
        self.lista_carrito = tk.Listbox(panel, width=34, height=10, font=FUENTE_LISTA, exportselection=False)
        self.lista_carrito.pack(padx=8, fill="x")

        fila = tk.Frame(panel)
        fila.pack(pady=6)
        tk.Label(fila, text="Nueva cantidad:").pack(side="left")
        self.nueva_cantidad = tk.Spinbox(fila, from_=1, to=100, width=5)
        self.nueva_cantidad.pack(side="left", padx=4)
        tk.Button(fila, text="Modificar cantidad", command=self.modificar).pack(side="left", padx=4)

        fila2 = tk.Frame(panel)
        fila2.pack(pady=2)
        tk.Label(fila2, text="ID o nombre:").pack(side="left")
        self.entrada_eliminar = tk.Entry(fila2, width=12)
        self.entrada_eliminar.pack(side="left", padx=4)
        tk.Button(fila2, text="Eliminar producto", command=self.eliminar).pack(side="left", padx=4)

        tk.Button(panel, text="Vaciar carrito", command=self.vaciar).pack(pady=6)

        self.etiqueta_totales = tk.Label(panel, text="", font=("Arial", 14, "bold"))
        self.etiqueta_totales.pack(pady=4)
        tk.Button(panel, text="Finalizar compra", fg=VERDE, font=("Arial", 14, "bold"),
                  command=self.finalizar).pack(pady=(0, 10))

    def actualizar_carrito(self):
        # R4: recorre la lista del carrito y muestra cantidad, subtotal y totales.
        self.lista_carrito.delete(0, "end")
        actual = self.carrito.items.primerNodo
        while actual is not None:
            item = actual.datos
            renglon = (str(item.producto.id).ljust(5) + item.producto.nombre[:13].ljust(14)
                       + str(item.cantidad).ljust(6) + "$" + str(item.subtotal()))
            self.lista_carrito.insert("end", renglon)
            actual = actual.siguienteNodo
        self.etiqueta_totales.config(text="Artículos: " + str(self.carrito.total_articulos())
                                     + "     TOTAL: $" + str(self.carrito.total_pagar()))

    def modificar(self):
        # R5: cambia la cantidad del producto seleccionado en el carrito.
        seleccion = self.lista_carrito.curselection()
        if len(seleccion) == 0:
            messagebox.showwarning("Modificar", "Selecciona un producto del carrito.")
            return
        cantidad = self.leer_cantidad(self.nueva_cantidad)
        if cantidad is None:
            messagebox.showerror("Dato no válido", "La cantidad debe ser un número entero de 1 a 100.")
            return
        item = obtener_en_posicion(self.carrito.items, seleccion[0])
        item.cantidad = cantidad
        self.actualizar_carrito()

    def eliminar(self):
        # R6: elimina por ID o por nombre. Si la caja está vacía, usa el producto seleccionado.
        texto = self.entrada_eliminar.get().strip()
        if texto.isdecimal():
            item = self.carrito.buscar_por_id(int(texto))
        elif texto != "":
            item = self.carrito.buscar_por_nombre(texto)
        else:
            seleccion = self.lista_carrito.curselection()
            if len(seleccion) == 0:
                messagebox.showwarning("Eliminar", "Escribe un ID o nombre, o selecciona un producto del carrito.")
                return
            item = obtener_en_posicion(self.carrito.items, seleccion[0])

        if item is None:
            messagebox.showerror("Eliminar", "Ese producto no está en el carrito.")
            return
        self.carrito.eliminar(item)
        self.entrada_eliminar.delete(0, "end")
        self.actualizar_carrito()

    def vaciar(self):
        # R7: pregunta y deja el carrito vacío para empezar otra compra.
        if self.carrito.esta_vacio():
            messagebox.showinfo("Vaciar", "El carrito ya está vacío.")
            return
        if messagebox.askyesno("Vaciar", "¿Seguro que quieres vaciar el carrito?"):
            self.carrito.vaciar()
            self.actualizar_carrito()

    def finalizar(self):
        # R8: muestra el ticket con los productos, los artículos y el total, y vacía el carrito.
        if self.carrito.esta_vacio():
            messagebox.showinfo("Finalizar compra", "No hay productos en el carrito.")
            return
        ticket = "TICKET DE COMPRA\n\n"
        actual = self.carrito.items.primerNodo
        while actual is not None:
            item = actual.datos
            ticket = (ticket + item.producto.nombre + ": " + str(item.cantidad) + " x $"
                      + str(item.producto.precio) + " = $" + str(item.subtotal()) + "\n")
            actual = actual.siguienteNodo
        ticket = ticket + "\nCantidad total de artículos: " + str(self.carrito.total_articulos())
        ticket = ticket + "\nMonto total a pagar: $" + str(self.carrito.total_pagar())
        ticket = ticket + "\n\n¡Gracias por su compra!"
        messagebox.showinfo("Finalizar compra", ticket)
        self.carrito.vaciar()
        self.actualizar_carrito()


if __name__ == "__main__":
    ventana_principal = tk.Tk()
    interfaz = VentanaCarrito(ventana_principal)
    ventana_principal.mainloop()
