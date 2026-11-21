import unittest
from sistema_archivos import SistemaArchivos


class PruebasSistemaArchivos(unittest.TestCase):
    def test_raiz_inicial(self):
        sistema = SistemaArchivos("Documentos")
        raiz = sistema.raiz

        self.assertEqual(raiz.nombre, "Documentos")
        self.assertEqual(raiz.tipo, "Directorio")
        self.assertEqual(raiz.tamano, 0)
        self.assertEqual(raiz.extension, "")

    def test_insercion_y_busqueda(self):
        sistema = SistemaArchivos("Documentos")
        sistema.insertar_directorio("  Apuntes  ")
        sistema.insertar_archivo("Agenda", ".txt", 5)

        directorio = sistema.buscar("apuntes")
        self.assertIsNotNone(directorio)
        self.assertEqual(directorio.nombre, "Apuntes")
        self.assertEqual(directorio.tipo, "Directorio")
        self.assertEqual(directorio.extension, "")
        self.assertEqual(directorio.tamano, 0)

        archivo = sistema.buscar("AGENDA")
        self.assertIsNotNone(archivo)
        self.assertEqual(archivo.nombre, "Agenda")
        self.assertEqual(archivo.tipo, "Archivo")
        self.assertEqual(archivo.extension, "txt")
        self.assertEqual(archivo.tamano, 5)

        mensaje = sistema.insertar_directorio("APUNTES")
        self.assertIn("ya existe", mensaje)
        nombres = [nodo.nombre for nodo in sistema.recorrido_inorden()]
        self.assertEqual(nombres, ["Agenda", "Apuntes", "Documentos"])

    def test_validaciones(self):
        sistema = SistemaArchivos("Documentos")

        self.assertIn("No se pudo insertar", sistema.insertar_directorio(""))
        self.assertIn("No se pudo insertar", sistema.insertar_archivo("SinExtension", "", 5))
        self.assertIn("No se pudo insertar", sistema.insertar_archivo("Negativo", "txt", -1))
        self.assertIn("No se pudo insertar", sistema.insertar_archivo("Decimal", "txt", 2.5))

        nombres = [nodo.nombre for nodo in sistema.recorrido_inorden()]
        self.assertEqual(nombres, ["Documentos"])

    def test_recorridos(self):
        sistema = SistemaArchivos("Documentos")
        sistema.insertar_directorio("Apuntes")
        sistema.insertar_directorio("Proyectos")
        sistema.insertar_archivo("Agenda", "txt", 5)
        sistema.insertar_archivo("Tarea", "txt", 10)

        inorden = [nodo.nombre for nodo in sistema.recorrido_inorden()]
        preorden = [nodo.nombre for nodo in sistema.recorrido_preorden()]
        postorden = [nodo.nombre for nodo in sistema.recorrido_postorden()]

        self.assertEqual(inorden, ["Agenda", "Apuntes", "Documentos", "Proyectos", "Tarea"])
        self.assertEqual(preorden, ["Documentos", "Apuntes", "Agenda", "Proyectos", "Tarea"])
        self.assertEqual(postorden, ["Agenda", "Apuntes", "Tarea", "Proyectos", "Documentos"])

    def test_eliminacion(self):
        sistema = SistemaArchivos("Documentos")
        sistema.insertar_directorio("Apuntes")
        sistema.insertar_archivo("Agenda", "txt", 5)

        self.assertIn("es la raíz", sistema.eliminar("Documentos"))
        self.assertIsNotNone(sistema.buscar("Documentos"))

        self.assertIn("el directorio tiene hijos", sistema.eliminar("Apuntes"))
        self.assertIsNotNone(sistema.buscar("Apuntes"))
        self.assertIsNotNone(sistema.buscar("Agenda"))

        self.assertIn("eliminado correctamente", sistema.eliminar("Agenda"))
        self.assertIsNone(sistema.buscar("Agenda"))

        self.assertIn("eliminado correctamente", sistema.eliminar("Apuntes"))
        self.assertIsNone(sistema.buscar("Apuntes"))

    def test_archivo_como_hoja(self):
        sistema = SistemaArchivos("M")
        sistema.insertar_archivo("T", "txt", 5)
        self.assertIsNotNone(sistema.buscar("T"))

        mensaje = sistema.insertar_directorio("Z")
        self.assertIn("el archivo 'T' no puede contener otros elementos", mensaje)
        self.assertIsNone(sistema.buscar("Z"))
