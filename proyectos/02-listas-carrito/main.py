# Proyecto de Listas - Carrito de compras
# Versión de consola: menú que conecta al usuario con el catálogo y el carrito.

from carrito import Catalogo, Carrito


class Tienda:
    """Conecta al usuario con el catálogo y el carrito mediante un menú."""

    def __init__(self):
        self.catalogo = Catalogo()
        self.carrito = Carrito()

    def leer_entero(self, mensaje, minimo, maximo):
        """Pide un número entero hasta que esté entre minimo y maximo."""
        while True:
            texto = input(mensaje).strip()
            try:
                numero = int(texto)
            except ValueError:
                print("  Error: escribe un número entero.")
                continue
            if numero < minimo or numero > maximo:
                print(f"  Error: el número debe estar entre {minimo} y {maximo}.")
            else:
                return numero

    def leer_texto(self, mensaje):
        """Pide un texto que no esté vacío."""
        texto = input(mensaje).strip()
        while texto == "":
            print("  Error: no puede quedar vacío.")
            texto = input(mensaje).strip()
        return texto

    def elegir_producto(self):
        """Pide un ID o un nombre y regresa el producto del catálogo, o None."""
        texto = self.leer_texto("ID o nombre del producto: ")
        if texto.isdigit():
            producto = self.catalogo.buscar_por_id(int(texto))
            if producto is None:
                print("  Error: no existe un producto con ese ID.")
            return producto

        encontrados = self.catalogo.buscar_por_nombre(texto)
        if encontrados.estaVacia():
            print("  Error: no hay productos con ese nombre.")
            return None
        # Si la lista de resultados solo tiene un nodo, ese es el producto.
        if encontrados.primerNodo == encontrados.ultimoNodo:
            return encontrados.primerNodo.datos

        print("  Hay varios productos con ese nombre:")
        actual = encontrados.primerNodo
        while actual is not None:
            actual.datos.mostrar()
            actual = actual.siguienteNodo
        id_producto = self.leer_entero("  Escribe el ID del que quieres: ", 1, 999)
        producto = self.catalogo.buscar_por_id(id_producto)
        if producto is None:
            print("  Error: no existe un producto con ese ID.")
        return producto

    def ver_catalogo(self):
        print("\nCATÁLOGO  (ID | Producto | Precio)")
        self.catalogo.mostrar()

    def buscar_producto(self):
        print("\n1) Buscar por ID   2) Buscar por nombre")
        opcion = self.leer_entero("Opción: ", 1, 2)
        if opcion == 1:
            producto = self.catalogo.buscar_por_id(self.leer_entero("ID: ", 1, 999))
            if producto is None:
                print("  No existe un producto con ese ID.")
            else:
                producto.mostrar()
        else:
            encontrados = self.catalogo.buscar_por_nombre(self.leer_texto("Nombre o parte del nombre: "))
            if encontrados.estaVacia():
                print("  No se encontraron productos.")
            actual = encontrados.primerNodo
            while actual is not None:
                actual.datos.mostrar()
                actual = actual.siguienteNodo

    def agregar_al_carrito(self):
        producto = self.elegir_producto()
        if producto is not None:
            cantidad = self.leer_entero("Cantidad: ", 1, 100)
            self.carrito.agregar(producto, cantidad)
            print(f"  Se agregaron {cantidad} x {producto.nombre} al carrito.")

    def ver_carrito(self):
        print("\nCARRITO  (ID | Producto | Cantidad x Precio = Subtotal)")
        if self.carrito.esta_vacio():
            print("  El carrito está vacío.")
        else:
            self.carrito.mostrar()

    def modificar_cantidad(self):
        if self.carrito.esta_vacio():
            print("  El carrito está vacío.")
            return
        self.ver_carrito()
        item = self.carrito.buscar_por_id(self.leer_entero("ID del producto a modificar: ", 1, 999))
        if item is None:
            print("  Error: ese producto no está en el carrito.")
            return
        nueva_cantidad = self.leer_entero("Nueva cantidad (0 para quitarlo): ", 0, 100)
        if nueva_cantidad == 0:
            self.carrito.eliminar(item)
            print("  Producto eliminado del carrito.")
        else:
            item.cantidad = nueva_cantidad
            print(f"  Cantidad actualizada. Nuevo subtotal: ${item.subtotal():.2f}")

    def eliminar_del_carrito(self):
        if self.carrito.esta_vacio():
            print("  El carrito está vacío.")
            return
        self.ver_carrito()
        texto = self.leer_texto("ID o nombre del producto a eliminar: ")
        if texto.isdigit():
            item = self.carrito.buscar_por_id(int(texto))
        else:
            item = self.carrito.buscar_por_nombre(texto)
        if item is None:
            print("  Error: ese producto no está en el carrito.")
        else:
            self.carrito.eliminar(item)
            print(f"  Se eliminó {item.producto.nombre} del carrito.")

    def vaciar_carrito(self):
        if self.carrito.esta_vacio():
            print("  El carrito ya está vacío.")
            return
        respuesta = input("¿Seguro que quieres vaciar el carrito? (s/n): ").strip().lower()
        if respuesta == "s":
            self.carrito.vaciar()
            print("  Carrito vaciado. Puedes empezar una nueva compra.")
        else:
            print("  No se vació el carrito.")

    def finalizar_compra(self):
        if self.carrito.esta_vacio():
            print("  No hay productos en el carrito.")
            return
        print("\n=========== TICKET DE COMPRA ===========")
        self.carrito.mostrar()
        print(f"  Cantidad total de artículos: {self.carrito.total_articulos()}")
        print(f"  Monto total a pagar: ${self.carrito.total_pagar():.2f}")
        print("  ¡Gracias por su compra!")
        self.carrito.vaciar()

    def mostrar_menu(self):
        print("\n========== CARRITO DE COMPRAS ==========")
        print("  1) Ver catálogo")
        print("  2) Buscar producto")
        print("  3) Agregar producto al carrito")
        print("  4) Ver carrito")
        print("  5) Modificar cantidad")
        print("  6) Eliminar producto del carrito")
        print("  7) Vaciar carrito")
        print("  8) Finalizar compra")
        print("  0) Salir")

    def ejecutar(self):
        """Muestra el menú y llama a la opción elegida hasta que el usuario sale."""
        opcion = -1
        while opcion != 0:
            self.mostrar_menu()
            opcion = self.leer_entero("Elige una opción: ", 0, 8)
            if opcion == 1:
                self.ver_catalogo()
            elif opcion == 2:
                self.buscar_producto()
            elif opcion == 3:
                self.agregar_al_carrito()
            elif opcion == 4:
                self.ver_carrito()
            elif opcion == 5:
                self.modificar_cantidad()
            elif opcion == 6:
                self.eliminar_del_carrito()
            elif opcion == 7:
                self.vaciar_carrito()
            elif opcion == 8:
                self.finalizar_compra()
        print("Hasta luego.")


if __name__ == "__main__":
    tienda = Tienda()
    tienda.ejecutar()
