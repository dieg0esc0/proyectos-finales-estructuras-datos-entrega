from sistema_archivos import SistemaArchivos


if __name__ == "__main__":
    sistema = SistemaArchivos("Documentos")
    sistema.insertar_directorio("Apuntes")
    sistema.insertar_directorio("Proyectos")
    sistema.insertar_archivo("Agenda", "txt", 5)
    sistema.insertar_archivo("Tarea", "txt", 10)

    print("Recorrido inorden")
    for nodo in sistema.recorrido_inorden():
        print(nodo.obtener_informacion())
        print()

    print("Recorrido preorden")
    for nodo in sistema.recorrido_preorden():
        print(nodo.obtener_informacion())
        print()

    print("Recorrido postorden")
    for nodo in sistema.recorrido_postorden():
        print(nodo.obtener_informacion())
        print()
