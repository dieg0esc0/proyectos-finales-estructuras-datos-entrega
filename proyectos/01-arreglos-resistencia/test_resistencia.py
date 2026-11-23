import unittest
from resistencia import Resistencia, Circuito, COLORES, MULTIPLICADORES


def colores_de(valor):
    # Regresa los colores de un valor, o "ERROR" si no se puede.
    resistencia = Resistencia(valor)
    if resistencia.calcular_colores():
        return resistencia.texto_colores()
    return "ERROR"


def circuito_con(valores):
    # Crea un circuito con valores fijos para revisar las fórmulas.
    circuito = Circuito(len(valores))
    for i in range(len(valores)):
        circuito.resistores[i] = valores[i]
    return circuito


class PruebasResistencia(unittest.TestCase):
    def test_arreglos_de_la_tabla(self):
        self.assertEqual(len(COLORES), 10)
        self.assertEqual(COLORES[6], "Azul")
        self.assertEqual(MULTIPLICADORES[2], 100)

    def test_ejemplos_del_proyecto(self):
        self.assertEqual(colores_de(160), "Marrón, Azul, Marrón")
        self.assertEqual(colores_de(5800), "Verde, Gris, Rojo")

    def test_otros_valores(self):
        self.assertEqual(colores_de(10), "Marrón, Negro, Negro")
        self.assertEqual(colores_de(47000), "Amarillo, Violeta, Naranja")
        self.assertEqual(colores_de(1000000000), "Marrón, Negro, Gris")

    def test_dorado_y_plateado(self):
        self.assertEqual(colores_de(1), "Marrón, Negro, Dorado")
        self.assertEqual(colores_de(4.7), "Amarillo, Violeta, Dorado")
        self.assertEqual(colores_de(0.47), "Amarillo, Violeta, Plateado")
        self.assertEqual(colores_de(0.1), "Marrón, Negro, Plateado")

    def test_valores_no_validos(self):
        self.assertEqual(colores_de(0.05), "ERROR")
        self.assertEqual(colores_de(4.75), "ERROR")
        self.assertEqual(colores_de(15.5), "ERROR")
        self.assertEqual(colores_de(165), "ERROR")
        self.assertEqual(colores_de(990000000000), "ERROR")

    def test_serie(self):
        self.assertEqual(circuito_con([100, 100, 50]).total_serie(), 250)

    def test_paralelo(self):
        circuito = circuito_con([100, 100, 50])
        self.assertAlmostEqual(circuito.suma_inversos(), 0.04)
        self.assertAlmostEqual(circuito.total_paralelo(), 25)

    def test_resistores_aleatorios(self):
        circuito = Circuito(50)
        circuito.generar_resistores()
        for i in range(circuito.n):
            self.assertTrue(circuito.resistores[i] >= 10)
            self.assertTrue(circuito.resistores[i] <= 1000000000)
