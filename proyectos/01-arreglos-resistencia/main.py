# Proyecto de Arreglos - Resistencia eléctrica
# Versión de consola del programa.

from resistencia import Resistencia, Circuito, MAXIMO_N


def mostrar_menu():
    print("\n=== RESISTENCIA ELÉCTRICA ===")
    print("1. Obtener los colores de una resistencia")
    print("2. Resistencias en serie y en paralelo")
    print("0. Salir")


def leer_entero(mensaje):
    # Pide un número entero hasta que el usuario escriba uno válido.
    while True:
        entrada = input(mensaje)
        try:
            return int(entrada)
        except ValueError:
            print("Escribe un número entero.")


def leer_decimal(mensaje):
    # Pide un número que puede tener decimales (por ejemplo 4.7 o 0.47).
    while True:
        entrada = input(mensaje)
        try:
            return float(entrada)
        except ValueError:
            print("Escribe un número, por ejemplo 160, 4.7 o 0.47.")


def obtener_colores():
    # R1: pide el valor y muestra los colores de la resistencia.
    valor = leer_decimal("Valor de la resistencia (ohmios): ")
    resistencia = Resistencia(valor)
    if resistencia.calcular_colores():
        print("Colores:", resistencia.texto_colores())
        print("Multiplicador: x" + str(resistencia.multiplicador))
    else:
        print(resistencia.error)


def calcular_circuito():
    # R2 y R3: pide n, genera los resistores y muestra serie y paralelo.
    n = leer_entero("Cantidad de resistencias n (1 a " + str(MAXIMO_N) + "): ")
    if n < 1 or n > MAXIMO_N:
        print("n debe estar entre 1 y " + str(MAXIMO_N) + ".")
        return

    circuito = Circuito(n)
    circuito.generar_resistores()
    for i in range(n):
        print("R" + str(i + 1) + " =", circuito.resistores[i], "ohmios")

    print("Serie: Rts =", circuito.total_serie(), "ohmios")
    print("Suma de inversos (resultado intermedio): 1/R1 + ... + 1/R" + str(n) + " =", circuito.suma_inversos())
    print("Paralelo: Rtp = 1 / (suma de inversos) =", round(circuito.total_paralelo(), 2), "ohmios")


def ejecutar_menu():
    opcion = -1
    while opcion != 0:
        mostrar_menu()
        opcion = leer_entero("Elige una opción: ")
        if opcion == 1:
            obtener_colores()
        elif opcion == 2:
            calcular_circuito()
        elif opcion == 0:
            print("Hasta luego.")
        else:
            print("Opción no válida")


if __name__ == "__main__":
    ejecutar_menu()
