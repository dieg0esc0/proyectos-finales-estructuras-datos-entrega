# Proyecto de Listas - Carrito de compras
# Versión de consola: menú que conecta al usuario con el catálogo y el carrito.

from carrito import Catalogo, Carrito


class Tienda:
    # Tiene el catálogo y el carrito, y muestra el menú.

    def __init__(self):
        self.catalogo = Catalogo()
        self.carrito = Carrito()

    def leer_entero(self, mensaje, minimo, maximo):
        # Pide un número entero hasta que esté entre minimo y maximo.
        while True:
            try:
                numero = int(input(mensaje))
                if numero >= minimo and numero <= maximo:
                    return numero
                print("  Error: el número debe estar entre", minimo, "y", maximo)
            except ValueError:
                print("  Error: escribe un número entero.")

    def ver_catalogo(self):
        print("\nCATÁLOGO  (ID | Producto | Precio)")
        self.catalogo.mostrar()

    def buscar_producto(self):
        # Busca en el catálogo por ID (si se escribe un número) o por nombre.
        texto = input("Escribe el ID o el nombre del producto: ")
        # isdecimal() solo acepta dígitos que int() sí puede convertir (isdigit() también acepta ²).
        if texto.isdecimal():
            producto = self.catalogo.buscar_por_id(int(texto))
        else:
            producto = self.catalogo.buscar_por_nombre(texto)

        if producto is None:
            print("  No se encontró el producto.")
        else:
            producto.mostrar()

    def agregar_al_carrito(self):
        id_producto = self.leer_entero("ID del producto: ", 1, 999)
        producto = self.catalogo.buscar_por_id(id_producto)
        if producto is None:
            print("  Error: no existe un producto con ese ID.")
            return
        cantidad = self.leer_entero("Cantidad: ", 1, 100)
        self.carrito.agregar(producto, cantidad)
        print("  Se agregó", producto.nombre, "al carrito.")

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
        id_producto = self.leer_entero("ID del producto a modificar: ", 1, 999)
        item = self.carrito.buscar_por_id(id_producto)
        if item is None:
            print("  Error: ese producto no está en el carrito.")
            return
        item.cantidad = self.leer_entero("Nueva cantidad: ", 1, 100)
        print("  Cantidad actualizada. Nuevo subtotal: $" + str(item.subtotal()))

    def eliminar_del_carrito(self):
        # Elimina por ID (si se escribe un número) o por nombre.
        if self.carrito.esta_vacio():
            print("  El carrito está vacío.")
            return
        self.ver_carrito()
        texto = input("Escribe el ID o el nombre del producto a eliminar: ")
        if texto.isdecimal():
            item = self.carrito.buscar_por_id(int(texto))
        else:
            item = self.carrito.buscar_por_nombre(texto)

        if item is None:
            print("  Error: ese producto no está en el carrito.")
        else:
            self.carrito.eliminar(item)
            print("  Se eliminó", item.producto.nombre, "del carrito.")

    def vaciar_carrito(self):
        if self.carrito.esta_vacio():
            print("  El carrito ya está vacío.")
            return
        respuesta = input("¿Seguro que quieres vaciar el carrito? (s/n): ")
        if respuesta == "s":
            self.carrito.vaciar()
            print("  Carrito vaciado. Puedes empezar una nueva compra.")
        else:
            print("  No se vació el carrito.")

    def finalizar_compra(self):
        if self.carrito.esta_vacio():
            print("  No hay productos en el carrito.")
            return
        print("\n========== TICKET DE COMPRA ==========")
        self.carrito.mostrar()
        print("  Cantidad total de artículos:", self.carrito.total_articulos())
        print("  Monto total a pagar: $" + str(self.carrito.total_pagar()))
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
        # Muestra el menú hasta que el usuario elige 0.
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
