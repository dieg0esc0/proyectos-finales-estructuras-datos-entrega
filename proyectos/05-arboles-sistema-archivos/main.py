from sistema_archivos import SistemaArchivos


if __name__ == "__main__":
    sistema = SistemaArchivos("  Documentos  ")
    print(f"Nombre guardado para la raíz: {sistema.raiz.nombre!r}")

    print("\nValidación de directorios:")
    print(sistema.insertar_directorio("  Apuntes  "))
    print(sistema.insertar_directorio(" "))
    print(sistema.insertar_directorio("  APUNTES  "))

    print("\nValidación de archivos:")
    print(sistema.insertar_archivo("Agenda", "txt", 5))
    print(sistema.insertar_archivo("Notas", "", 5))
    print(sistema.insertar_archivo("Tarea", ".txt", 10))
    tarea = sistema.buscar("  TAREA  ")
    if tarea is not None:
        print(f"Extensión guardada para '{tarea.nombre}': {tarea.extension!r}")
    print(sistema.insertar_archivo("Borrador", "txt", -1))
    print(sistema.insertar_archivo("Borrador", "txt", 2.5))

    print("\nBúsqueda y eliminación:")
    print("Buscar con nombre vacío:", sistema.buscar(""))
    print(sistema.eliminar(""))
    print(sistema.eliminar("  documentos  "))
    print(sistema.eliminar("Apuntes"))

    print("\nInorden antes de eliminar:")
    for nodo in sistema.recorrido_inorden():
        print(f"- {nodo.nombre} ({nodo.tipo})")

    print()
    print(sistema.eliminar("  agenda  "))
    print("Buscar 'Agenda' después de eliminar:", sistema.buscar("Agenda"))
    print(sistema.eliminar("Apuntes"))

    print("\nInorden después de eliminar:")
    for nodo in sistema.recorrido_inorden():
        print(f"- {nodo.nombre} ({nodo.tipo})")
