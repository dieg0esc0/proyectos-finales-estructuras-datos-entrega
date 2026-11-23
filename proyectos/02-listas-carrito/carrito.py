# Proyecto de Listas - Carrito de compras
# Clases del problema: Producto, ItemCarrito, Catalogo y Carrito.
# El catálogo y el carrito guardan sus datos en una Lista enlazada.

from lista import Lista


class Producto:
    # Producto de la tienda: ID, nombre y precio.

    def __init__(self, id_producto, nombre, precio):
        self.id = id_producto
        self.nombre = nombre
        self.precio = precio

    def mostrar(self):
        print("  ", self.id, "|", self.nombre, "| $" + str(self.precio))


class ItemCarrito:
    # Renglón del carrito: el producto y la cantidad que se va a comprar.

    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    def subtotal(self):
        # Precio por cantidad. Se calcula cada vez, así siempre está actualizado.
        return self.producto.precio * self.cantidad

    def mostrar(self):
        print("  ", self.producto.id, "|", self.producto.nombre, "|", self.cantidad,
              "x $" + str(self.producto.precio), "= $" + str(self.subtotal()))


class Catalogo:
    # Lista enlazada con los productos de la tienda.

    def __init__(self):
        self.productos = Lista()
        self.productos.insertarAlFinal(Producto(101, "Laptop", 12999))
        self.productos.insertarAlFinal(Producto(102, "Mouse", 250))
        self.productos.insertarAlFinal(Producto(103, "Teclado", 899))
        self.productos.insertarAlFinal(Producto(104, "Audifonos", 650))
        self.productos.insertarAlFinal(Producto(105, "Memoria USB", 189))
        self.productos.insertarAlFinal(Producto(106, "Monitor", 2799))
        self.productos.insertarAlFinal(Producto(107, "Cable HDMI", 129))
        self.productos.insertarAlFinal(Producto(108, "Mochila", 559))
        self.productos.insertarAlFinal(Producto(109, "Cuaderno", 45))
        self.productos.insertarAlFinal(Producto(110, "Plumas", 80))

    def mostrar(self):
        # Recorre la lista desde el primer nodo e imprime cada producto.
        actual = self.productos.primerNodo
        while actual is not None:
            actual.datos.mostrar()
            actual = actual.siguienteNodo

    def buscar_por_id(self, id_producto):
        # Recorre la lista y regresa el producto con ese ID, o None si no existe.
        actual = self.productos.primerNodo
        while actual is not None:
            if actual.datos.id == id_producto:
                return actual.datos
            actual = actual.siguienteNodo
        return None

    def buscar_por_nombre(self, nombre):
        # Recorre la lista y regresa el producto con ese nombre, o None si no existe.
        # No importa si se escribe con mayúsculas o minúsculas.
        actual = self.productos.primerNodo
        while actual is not None:
            if actual.datos.nombre.lower() == nombre.lower():
                return actual.datos
            actual = actual.siguienteNodo
        return None


class Carrito:
    # Lista enlazada con los renglones (ItemCarrito) que se van a comprar.

    def __init__(self):
        self.items = Lista()

    def esta_vacio(self):
        return self.items.estaVacia()

    def buscar_por_id(self, id_producto):
        # Regresa el renglón del producto con ese ID, o None si no está en el carrito.
        actual = self.items.primerNodo
        while actual is not None:
            if actual.datos.producto.id == id_producto:
                return actual.datos
            actual = actual.siguienteNodo
        return None

    def buscar_por_nombre(self, nombre):
        # Regresa el renglón del producto con ese nombre, o None si no está en el carrito.
        actual = self.items.primerNodo
        while actual is not None:
            if actual.datos.producto.nombre.lower() == nombre.lower():
                return actual.datos
            actual = actual.siguienteNodo
        return None

    def agregar(self, producto, cantidad):
        # Si el producto ya está en el carrito se suma la cantidad.
        # Si no está, se agrega un renglón nuevo al final de la lista.
        item = self.buscar_por_id(producto.id)
        if item is not None:
            item.cantidad = item.cantidad + cantidad
        else:
            self.items.insertarAlFinal(ItemCarrito(producto, cantidad))

    def eliminar(self, item):
        self.items.eliminar(item)

    def vaciar(self):
        self.items.vaciar()

    def total_articulos(self):
        # Suma las cantidades de todos los renglones.
        total = 0
        actual = self.items.primerNodo
        while actual is not None:
            total = total + actual.datos.cantidad
            actual = actual.siguienteNodo
        return total

    def total_pagar(self):
        # Suma los subtotales de todos los renglones.
        total = 0
        actual = self.items.primerNodo
        while actual is not None:
            total = total + actual.datos.subtotal()
            actual = actual.siguienteNodo
        return total

    def mostrar(self):
        # Imprime cada renglón y al final los totales.
        actual = self.items.primerNodo
        while actual is not None:
            actual.datos.mostrar()
            actual = actual.siguienteNodo
        print("  ----------------------------------------")
        print("   Artículos:", self.total_articulos(), "  Total: $" + str(self.total_pagar()))
