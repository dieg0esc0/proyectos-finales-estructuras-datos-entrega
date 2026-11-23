import unittest
from lista import Lista, ExcepcionListaVacia
from carrito import Catalogo, Carrito


def contenido(lista):
    datos = []
    actual = lista.primerNodo
    while actual is not None:
        datos.append(actual.datos)
        actual = actual.siguienteNodo
    return datos


def lista_con(datos):
    lista = Lista("prueba")
    for dato in datos:
        lista.insertarAlFinal(dato)
    return lista


def carrito_con(catalogo, ids_y_cantidades):
    carrito = Carrito()
    for i in range(0, len(ids_y_cantidades), 2):
        carrito.agregar(catalogo.buscar_por_id(ids_y_cantidades[i]), ids_y_cantidades[i + 1])
    return carrito


class PruebasLista(unittest.TestCase):
    def test_lista_vacia(self):
        lista = Lista("prueba")
        self.assertTrue(lista.estaVacia())
        with self.assertRaises(ExcepcionListaVacia):
            lista.eliminarDelFrente()

    def test_insertar_al_final(self):
        lista = lista_con(["A", "B", "C"])
        self.assertEqual(contenido(lista), ["A", "B", "C"])
        self.assertEqual(lista.ultimoNodo.datos, "C")

    def test_eliminar_del_frente_y_del_final(self):
        lista = lista_con(["A", "B", "C"])
        self.assertEqual(lista.eliminarDelFrente(), "A")
        self.assertEqual(lista.eliminarDelFinal(), "C")
        self.assertEqual(lista.primerNodo, lista.ultimoNodo)

    def test_eliminar_de_en_medio_y_vaciar(self):
        lista = lista_con(["A", "B", "C", "D"])
        lista.eliminar("C")
        self.assertEqual(contenido(lista), ["A", "B", "D"])
        lista.eliminar("D")
        self.assertEqual(lista.ultimoNodo.datos, "B")
        lista.vaciar()
        self.assertTrue(lista.estaVacia())
        self.assertIsNone(lista.ultimoNodo)


class PruebasCarrito(unittest.TestCase):
    def test_catalogo_y_busqueda(self):
        catalogo = Catalogo()
        self.assertEqual(len(contenido(catalogo.productos)), 10)
        self.assertEqual(catalogo.buscar_por_id(106).nombre, "Monitor 24 pulgadas")
        self.assertIsNone(catalogo.buscar_por_id(999))
        self.assertEqual(len(contenido(catalogo.buscar_por_nombre("CABLE"))), 1)
        self.assertEqual(len(contenido(catalogo.buscar_por_nombre("laptop"))), 2)
        self.assertTrue(catalogo.buscar_por_nombre("xyz").estaVacia())

    def test_agregar_y_totales(self):
        catalogo = Catalogo()
        carrito = carrito_con(catalogo, [101, 1, 102, 2])
        self.assertEqual(len(contenido(carrito.items)), 2)
        self.assertEqual(carrito.buscar_por_id(102).subtotal(), 499.00)
        self.assertEqual(carrito.total_articulos(), 3)
        self.assertEqual(carrito.total_pagar(), 13498.00)
        carrito.agregar(catalogo.buscar_por_id(102), 3)
        self.assertEqual(carrito.buscar_por_id(102).cantidad, 5)
        self.assertEqual(len(contenido(carrito.items)), 2)

    def test_modificar_cantidad(self):
        carrito = carrito_con(Catalogo(), [102, 2, 105, 1])
        carrito.buscar_por_id(102).cantidad = 5
        self.assertEqual(carrito.buscar_por_id(102).subtotal(), 1247.50)
        self.assertEqual(carrito.total_pagar(), 1436.50)

    def test_eliminar_por_id_y_nombre(self):
        carrito = carrito_con(Catalogo(), [101, 1, 103, 1, 107, 2])
        carrito.eliminar(carrito.buscar_por_id(103))
        self.assertIsNone(carrito.buscar_por_id(103))
        carrito.eliminar(carrito.buscar_por_nombre("CABLE HDMI 2 m"))
        self.assertIsNone(carrito.buscar_por_id(107))
        self.assertEqual(carrito.total_articulos(), 1)
        self.assertIsNone(carrito.buscar_por_nombre("xyz"))

    def test_vaciar_y_finalizar(self):
        carrito = carrito_con(Catalogo(), [101, 1, 102, 2, 109, 5])
        self.assertEqual(carrito.total_articulos(), 8)
        self.assertEqual(carrito.total_pagar(), 13725.50)
        carrito.vaciar()
        self.assertTrue(carrito.esta_vacio())
        self.assertEqual(carrito.total_pagar(), 0)
