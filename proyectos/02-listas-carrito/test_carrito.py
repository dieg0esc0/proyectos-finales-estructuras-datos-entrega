import unittest
from lista import Lista
from carrito import Catalogo, Carrito


def contenido(lista):
    # Recorre la lista y regresa sus datos en orden.
    datos = []
    actual = lista.primerNodo
    while actual is not None:
        datos.append(actual.datos)
        actual = actual.siguienteNodo
    return datos


class PruebasLista(unittest.TestCase):
    def test_lista_nueva_vacia(self):
        self.assertTrue(Lista().estaVacia())

    def test_insertar_al_final(self):
        lista = Lista()
        lista.insertarAlFinal("A")
        lista.insertarAlFinal("B")
        lista.insertarAlFinal("C")
        self.assertEqual(contenido(lista), ["A", "B", "C"])
        self.assertEqual(lista.ultimoNodo.datos, "C")

    def test_eliminar(self):
        lista = Lista()
        for letra in ["A", "B", "C", "D"]:
            lista.insertarAlFinal(letra)
        lista.eliminar("B")
        self.assertEqual(contenido(lista), ["A", "C", "D"])
        lista.eliminar("A")
        self.assertEqual(contenido(lista), ["C", "D"])
        lista.eliminar("D")
        self.assertEqual(contenido(lista), ["C"])
        self.assertEqual(lista.ultimoNodo.datos, "C")
        self.assertFalse(lista.eliminar("Z"))

    def test_vaciar(self):
        lista = Lista()
        lista.insertarAlFinal("A")
        lista.vaciar()
        self.assertTrue(lista.estaVacia())


class PruebasCarrito(unittest.TestCase):
    def test_catalogo_y_busqueda(self):
        catalogo = Catalogo()
        self.assertEqual(len(contenido(catalogo.productos)), 10)
        self.assertEqual(catalogo.buscar_por_id(106).nombre, "Monitor")
        self.assertEqual(catalogo.buscar_por_nombre("mouse").id, 102)
        self.assertIsNone(catalogo.buscar_por_id(999))
        self.assertIsNone(catalogo.buscar_por_nombre("xyz"))

    def test_agregar_y_totales(self):
        catalogo = Catalogo()
        carrito = Carrito()
        carrito.agregar(catalogo.buscar_por_id(101), 1)
        carrito.agregar(catalogo.buscar_por_id(102), 2)
        self.assertEqual(carrito.buscar_por_id(102).subtotal(), 500)
        self.assertEqual(carrito.total_articulos(), 3)
        self.assertEqual(carrito.total_pagar(), 13499)
        carrito.agregar(catalogo.buscar_por_id(102), 3)
        self.assertEqual(carrito.buscar_por_id(102).cantidad, 5)

    def test_modificar_cantidad(self):
        catalogo = Catalogo()
        carrito = Carrito()
        carrito.agregar(catalogo.buscar_por_id(102), 2)
        carrito.buscar_por_id(102).cantidad = 5
        self.assertEqual(carrito.buscar_por_id(102).subtotal(), 1250)
        self.assertEqual(carrito.total_pagar(), 1250)

    def test_eliminar_por_id_y_nombre(self):
        catalogo = Catalogo()
        carrito = Carrito()
        carrito.agregar(catalogo.buscar_por_id(101), 1)
        carrito.agregar(catalogo.buscar_por_id(103), 1)
        carrito.agregar(catalogo.buscar_por_id(107), 2)
        carrito.eliminar(carrito.buscar_por_id(103))
        self.assertIsNone(carrito.buscar_por_id(103))
        carrito.eliminar(carrito.buscar_por_nombre("cable hdmi"))
        self.assertIsNone(carrito.buscar_por_id(107))
        self.assertEqual(carrito.total_articulos(), 1)

    def test_vaciar(self):
        catalogo = Catalogo()
        carrito = Carrito()
        carrito.agregar(catalogo.buscar_por_id(101), 1)
        carrito.vaciar()
        self.assertTrue(carrito.esta_vacio())
        self.assertEqual(carrito.total_pagar(), 0)
