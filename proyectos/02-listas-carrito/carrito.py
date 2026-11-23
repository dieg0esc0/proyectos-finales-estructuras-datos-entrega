# Proyecto de Listas - Carrito de compras
# Clases del problema: Producto, ItemCarrito, Catalogo y Carrito.
# El catálogo y el carrito guardan sus datos en una Lista enlazada.

from lista import Lista


class Producto:
    """Producto del catálogo: ID, nombre y precio."""

    def __init__(self, id_producto, nombre, precio):
        self.id = id_producto
        self.nombre = nombre
        self.precio = precio

    def mostrar(self):
        """Imprime los datos del producto en un renglón."""
        print(f"  {self.id} | {self.nombre} | ${self.precio:.2f}")


class ItemCarrito:
    """Renglón del carrito: el producto y la cantidad que se va a comprar."""

    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    def subtotal(self):
        """Precio unitario por cantidad. Se calcula cada vez para que siempre esté actualizado."""
        return self.producto.precio * self.cantidad

    def mostrar(self):
        """Imprime el renglón con cantidad, precio unitario y subtotal."""
        print(f"  {self.producto.id} | {self.producto.nombre} | {self.cantidad} x "
              f"${self.producto.precio:.2f} = ${self.subtotal():.2f}")


class Catalogo:
    """Lista enlazada con los productos de la tienda."""

    def __init__(self):
        self.productos = Lista("catálogo")
        self.precargar()

    def precargar(self):
        """Inserta los productos con los que inicia la tienda."""
        self.productos.insertarAlFinal(Producto(101, "Laptop 14 pulgadas", 12999.00))
        self.productos.insertarAlFinal(Producto(102, "Mouse inalámbrico", 249.50))
        self.productos.insertarAlFinal(Producto(103, "Teclado mecánico", 899.00))
        self.productos.insertarAlFinal(Producto(104, "Audífonos Bluetooth", 649.90))
        self.productos.insertarAlFinal(Producto(105, "Memoria USB 64 GB", 189.00))
        self.productos.insertarAlFinal(Producto(106, "Monitor 24 pulgadas", 2799.00))
        self.productos.insertarAlFinal(Producto(107, "Cable HDMI 2 m", 129.00))
        self.productos.insertarAlFinal(Producto(108, "Mochila para laptop", 559.00))
        self.productos.insertarAlFinal(Producto(109, "Cuaderno profesional", 45.50))
        self.productos.insertarAlFinal(Producto(110, "Pluma de gel (paquete)", 79.90))

    def mostrar(self):
        """Recorre la lista e imprime todos los productos."""
        actual = self.productos.primerNodo
        while actual is not None:
            actual.datos.mostrar()
            actual = actual.siguienteNodo

    def buscar_por_id(self, id_producto):
        """Recorre la lista y regresa el producto con ese ID, o None si no existe."""
        actual = self.productos.primerNodo
        while actual is not None:
            if actual.datos.id == id_producto:
                return actual.datos
            actual = actual.siguienteNodo
        return None

    def buscar_por_nombre(self, texto):
        """Regresa una lista nueva con los productos cuyo nombre contiene el texto."""
        encontrados = Lista("resultados")
        actual = self.productos.primerNodo
        while actual is not None:
            if texto.lower() in actual.datos.nombre.lower():
                encontrados.insertarAlFinal(actual.datos)
            actual = actual.siguienteNodo
        return encontrados


class Carrito:
    """Lista enlazada con los renglones (ItemCarrito) que el cliente va a comprar."""

    def __init__(self):
        self.items = Lista("carrito")

    def esta_vacio(self):
        return self.items.estaVacia()

    def buscar_por_id(self, id_producto):
        """Regresa el renglón del producto con ese ID, o None si no está en el carrito."""
        actual = self.items.primerNodo
        while actual is not None:
            if actual.datos.producto.id == id_producto:
                return actual.datos
            actual = actual.siguienteNodo
        return None

    def buscar_por_nombre(self, nombre):
        """Regresa el renglón del producto con ese nombre exacto, o None."""
        actual = self.items.primerNodo
        while actual is not None:
            if actual.datos.producto.nombre.lower() == nombre.lower():
                return actual.datos
            actual = actual.siguienteNodo
        return None

    def agregar(self, producto, cantidad):
        """Si el producto ya está en el carrito suma la cantidad; si no, lo inserta al final."""
        item = self.buscar_por_id(producto.id)
        if item is not None:
            item.cantidad = item.cantidad + cantidad
        else:
            self.items.insertarAlFinal(ItemCarrito(producto, cantidad))

    def eliminar(self, item):
        """Quita un renglón del carrito."""
        self.items.eliminar(item)

    def vaciar(self):
        self.items.vaciar()

    def total_articulos(self):
        """Suma las cantidades de todos los renglones."""
        total = 0
        actual = self.items.primerNodo
        while actual is not None:
            total = total + actual.datos.cantidad
            actual = actual.siguienteNodo
        return total

    def total_pagar(self):
        """Suma los subtotales de todos los renglones."""
        total = 0
        actual = self.items.primerNodo
        while actual is not None:
            total = total + actual.datos.subtotal()
            actual = actual.siguienteNodo
        return total

    def mostrar(self):
        """Imprime cada renglón y al final los totales."""
        actual = self.items.primerNodo
        while actual is not None:
            actual.datos.mostrar()
            actual = actual.siguienteNodo
        print("  ----------------------------------------------")
        print(f"  Artículos: {self.total_articulos()}    Total: ${self.total_pagar():.2f}")
