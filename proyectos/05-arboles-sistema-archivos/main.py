from sistema_archivos import SistemaArchivos


if __name__ == "__main__":
    sistema = SistemaArchivos("Documentos")
    sistema.insertar_directorio("Apuntes")
    sistema.insertar_directorio("Proyectos")
    sistema.insertar_archivo("Agenda", "txt", 5)
    sistema.insertar_archivo("Tarea", "txt", 10)

    print("Inorden antes de eliminar:")
    for nodo in sistema.recorrido_inorden():
        print(f"- {nodo.nombre} ({nodo.tipo})")

    print("\nIntentos de eliminación:")
    print(sistema.eliminar("Documentos"))
    print(sistema.eliminar("Fotos"))
    print(sistema.eliminar("Apuntes"))
    print(sistema.eliminar("agenda"))

    if sistema.buscar("Agenda") is None:
        print("Búsqueda de 'Agenda': el archivo ya no existe.")
    else:
        print("Búsqueda de 'Agenda': el archivo todavía existe.")

    print(sistema.eliminar("Apuntes"))

    print("\nInorden después de eliminar:")
    for nodo in sistema.recorrido_inorden():
        print(f"- {nodo.nombre} ({nodo.tipo})")
