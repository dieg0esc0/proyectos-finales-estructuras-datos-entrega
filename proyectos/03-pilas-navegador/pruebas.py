from pila import Pila
from navegador import Navegador, CAPACIDAD
from urls import normalizar_url, obtener_descripcion, clave_pagina


class Revisor:
    def __init__(self):
        self.correctas = 0
        self.total = 0

    def titulo(self, texto):
        print("")
        print(texto)

    def revisar(self, nombre, condicion):
        self.total = self.total + 1
        if condicion:
            self.correctas = self.correctas + 1
            print("  [OK]     " + nombre)
        else:
            print("  [FALLO]  " + nombre)


def navegador_con_paginas(paginas):
    navegador = Navegador()
    for url in paginas:
        navegador.visitar(url)
    return navegador


def probar_pila(revisor):
    revisor.titulo("Estructura de datos: Pila (LIFO)")
    pila = Pila(4)
    revisor.revisar("una pila nueva está vacía", pila.esta_vacia())
    revisor.revisar("pop en pila vacía regresa None sin error", pila.pop() is None)
    revisor.revisar("peek en pila vacía regresa None sin error", pila.peek() is None)
    pila.push("a")
    pila.push("b")
    pila.push("c")
    revisor.revisar("peek regresa el último que entró", pila.peek() == "c")
    revisor.revisar("pop saca en orden LIFO", pila.pop() == "c" and pila.pop() == "b")
    pila.push("x")
    pila.push("y")
    pila.push("z")
    revisor.revisar("la pila se llena con 4 elementos", pila.esta_llena())
    revisor.revisar("push en pila llena regresa False", pila.push("w") == False)
    revisor.revisar("obtener_elementos va del tope al fondo", pila.obtener_elementos() == ["z", "y", "x", "a"])
    pila.vaciar()
    revisor.revisar("vaciar deja la pila en 0", pila.esta_vacia() and pila.tamano == 0)


def probar_visitar(revisor):
    revisor.titulo("R1. Visitar una página nueva")
    navegador = Navegador()
    navegador.visitar("https://www.google.com")
    revisor.revisar("la primera página no se guarda en la pila atrás", navegador.pila_atras.esta_vacia())
    navegador.visitar("https://www.mozilla.org")
    revisor.revisar("la página anterior se guarda en la pila atrás", navegador.pila_atras.peek() == "https://www.google.com")
    revisor.revisar("la página nueva pasa a ser la actual", navegador.pagina_actual == "https://www.mozilla.org")
    revisor.revisar("visitar la misma página no la duplica", navegador.visitar("https://www.mozilla.org") == "MISMA")


def probar_retroceder(revisor):
    revisor.titulo("R2. Retroceder (Back)")
    navegador = navegador_con_paginas(["https://www.google.com", "https://www.mozilla.org", "https://openai.com"])
    navegador.retroceder()
    revisor.revisar("la página actual pasa a la pila adelante", navegador.pila_adelante.peek() == "https://openai.com")
    revisor.revisar("el tope de la pila atrás pasa a ser la actual", navegador.pagina_actual == "https://www.mozilla.org")
    navegador.retroceder()
    revisor.revisar("se puede regresar hasta la primera página", navegador.pagina_actual == "https://www.google.com")


def probar_avanzar(revisor):
    revisor.titulo("R3. Avanzar (Forward)")
    navegador = navegador_con_paginas(["https://www.google.com", "https://www.mozilla.org", "https://openai.com"])
    navegador.retroceder()
    navegador.retroceder()
    navegador.avanzar()
    revisor.revisar("la página actual regresa a la pila atrás", navegador.pila_atras.peek() == "https://www.google.com")
    revisor.revisar("el tope de la pila adelante pasa a ser la actual", navegador.pagina_actual == "https://www.mozilla.org")
    navegador.avanzar()
    revisor.revisar("se puede avanzar hasta la última página", navegador.pagina_actual == "https://openai.com")


def probar_pagina_actual(revisor):
    revisor.titulo("R4. Página actual")
    navegador = Navegador()
    revisor.revisar("al inicio no hay página actual", navegador.pagina_actual is None)
    navegador.visitar("https://stackoverflow.com")
    revisor.revisar("la descripción de una página conocida", obtener_descripcion(navegador.pagina_actual) == "Bienvenido a Stack Overflow")
    revisor.revisar("la descripción de una página desconocida", obtener_descripcion("https://ejemplo.com") == "Bienvenido a ejemplo.com")


def probar_errores(revisor):
    revisor.titulo("R6. Evitar errores (pila vacía y pila llena)")
    navegador = Navegador()
    revisor.revisar("Back sin páginas regresa VACIA", navegador.retroceder() == "VACIA")
    revisor.revisar("Forward sin páginas regresa VACIA", navegador.avanzar() == "VACIA")
    navegador = navegador_con_paginas(["https://a.com", "https://b.com", "https://c.com", "https://d.com", "https://e.com"])
    revisor.revisar("la pila atrás se llena con " + str(CAPACIDAD) + " páginas", navegador.pila_atras.esta_llena())
    revisor.revisar("visitar con la pila llena regresa LLENA", navegador.visitar("https://f.com") == "LLENA")
    revisor.revisar("con la pila llena la página actual no cambia", navegador.pagina_actual == "https://e.com")


def probar_limpiar(revisor):
    revisor.titulo("R7. Limpiar la pila adelante al visitar")
    navegador = navegador_con_paginas(["https://www.google.com", "https://www.mozilla.org", "https://openai.com"])
    navegador.retroceder()
    navegador.retroceder()
    revisor.revisar("después de dos Back hay 2 páginas adelante", navegador.pila_adelante.tamano == 2)
    navegador.visitar("https://github.com")
    revisor.revisar("al visitar se vacía la pila adelante", navegador.pila_adelante.esta_vacia())
    revisor.revisar("después de visitar, Forward regresa VACIA", navegador.avanzar() == "VACIA")


def probar_urls(revisor):
    revisor.titulo("R8. Validación de la URL (auditoría)")
    revisor.revisar("URL vacía no es válida", normalizar_url("   ") is None)
    revisor.revisar("URL con espacios no es válida", normalizar_url("hola mundo") is None)
    revisor.revisar("URL sin punto no es válida", normalizar_url("hola") is None)
    revisor.revisar("URL con caracteres raros no es válida", normalizar_url("goo<gle.com") is None)
    revisor.revisar("se agrega https:// si no lo tiene", normalizar_url("google.com") == "https://google.com")
    revisor.revisar("acepta HTTPS:// en mayúsculas", normalizar_url("HTTPS://www.Mozilla.org") == "https://www.mozilla.org")
    revisor.revisar("quita la diagonal final", normalizar_url("https://github.com/") == "https://github.com")
    revisor.revisar("con y sin www es la misma página", clave_pagina("https://www.google.com") == clave_pagina("https://google.com"))
    navegador = navegador_con_paginas(["https://www.google.com"])
    revisor.revisar("google.com/ no se guarda dos veces", navegador.visitar(normalizar_url("google.com/")) == "MISMA")


revisor_principal = Revisor()
print("PRUEBAS DEL PROYECTO DE PILAS - NAVEGADOR WEB")
probar_pila(revisor_principal)
probar_visitar(revisor_principal)
probar_retroceder(revisor_principal)
probar_avanzar(revisor_principal)
probar_pagina_actual(revisor_principal)
probar_errores(revisor_principal)
probar_limpiar(revisor_principal)
probar_urls(revisor_principal)
print("")
print("Pruebas correctas: " + str(revisor_principal.correctas) + " de " + str(revisor_principal.total))
if revisor_principal.correctas == revisor_principal.total:
    print("Todas las pruebas se ejecutaron correctamente.")
else:
    print("Hay pruebas que fallaron, revisa los mensajes de arriba.")
