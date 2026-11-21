from sistema_archivos import SistemaArchivos


def mostrar_menu():
    print("\n=== SISTEMA DE ARCHIVOS ===")
    print("1. Crear directorio")
    print("2. Insertar archivo")
    print("3. Buscar elemento")
    print("4. Eliminar elemento")
    print("5. Mostrar información de un elemento")
    print("6. Recorrido inorden")
    print("7. Recorrido preorden")
    print("8. Recorrido postorden")
    print("0. Salir")


def leer_entero(mensaje):
    while True:
        entrada = input(mensaje)
        try:
            return int(entrada)
        except ValueError:
            print("Escribe un número entero.")


def mostrar_recorrido(nombre, nodos):
    print(f"\nRecorrido {nombre}:")
    if not nodos:
        print("No hay elementos para mostrar.")
        return

    for nodo in nodos:
        print(nodo.obtener_informacion())
        print()


def ejecutar_menu():
    sistema = SistemaArchivos("Documentos")

    while True:
        mostrar_menu()
        opcion = leer_entero("Elige una opción: ")

        if opcion == 1:
            nombre = input("Nombre del directorio: ")
            print(sistema.insertar_directorio(nombre))
        elif opcion == 2:
            nombre = input("Nombre del archivo: ")
            extension = input("Extensión: ")
            tamano = leer_entero("Tamaño: ")
            print(sistema.insertar_archivo(nombre, extension, tamano))
        elif opcion == 3:
            nombre = input("Nombre del elemento: ")
            nodo = sistema.buscar(nombre)
            if nodo is None:
                print("Elemento no encontrado")
            else:
                print(f"Elemento encontrado: {nodo.nombre} ({nodo.tipo})")
        elif opcion == 4:
            nombre = input("Nombre del elemento: ")
            print(sistema.eliminar(nombre))
        elif opcion == 5:
            nombre = input("Nombre del elemento: ")
            nodo = sistema.buscar(nombre)
            if nodo is None:
                print("Elemento no encontrado")
            else:
                print(nodo.obtener_informacion())
        elif opcion == 6:
            mostrar_recorrido("inorden", sistema.recorrido_inorden())
        elif opcion == 7:
            mostrar_recorrido("preorden", sistema.recorrido_preorden())
        elif opcion == 8:
            mostrar_recorrido("postorden", sistema.recorrido_postorden())
        elif opcion == 0:
            print("Hasta luego.")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    ejecutar_menu()
