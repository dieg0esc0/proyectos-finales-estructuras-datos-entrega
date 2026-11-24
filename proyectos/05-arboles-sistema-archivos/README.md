# Sistema de Archivos con Árbol Binario de Búsqueda

## Descripción

Este proyecto simula un sistema de archivos mediante un árbol binario de búsqueda (ABB). Empieza con el directorio raíz `Documentos`. Los archivos y directorios se ordenan alfabéticamente por su nombre, sin distinguir mayúsculas y minúsculas.

## Funcionalidades

- Crear directorios.
- Insertar archivos con nombre, extensión y tamaño.
- Buscar elementos sin distinguir mayúsculas y minúsculas.
- Mostrar la información de archivos y directorios.
- Eliminar archivos y directorios vacíos.
- Proteger la raíz y los directorios que todavía tienen hijos.
- Ejecutar recorridos inorden, preorden y postorden.
- Usar un menú de consola o una interfaz gráfica con Tkinter.
- Ver los nodos y sus conexiones en la interfaz gráfica.
- Ejecutar pruebas automatizadas con `unittest`.

## Reglas del árbol

- Al comparar con el nodo actual, los nombres alfabéticamente menores van a la izquierda y los mayores van a la derecha.
- La comparación usa el nombre sin distinguir mayúsculas y minúsculas. `Apuntes` y `APUNTES` cuentan como el mismo nombre, por lo que no se pueden insertar ambos.
- Los directorios pueden tener hijos. Los archivos siempre son hojas y no pueden contener elementos.
- La raíz no se puede eliminar. Un directorio solo se puede eliminar cuando no tiene hijos.

## Estructura de archivos

| Archivo | Responsabilidad |
| --- | --- |
| [`nodo.py`](nodo.py) | Define los datos de cada nodo y cómo presentar su información. |
| [`sistema_archivos.py`](sistema_archivos.py) | Contiene la lógica del árbol, las validaciones, la inserción, la búsqueda, la eliminación y los recorridos. |
| [`main.py`](main.py) | Proporciona el menú de consola. |
| [`interfaz.py`](interfaz.py) | Proporciona la interfaz gráfica con Tkinter y dibuja el árbol. |
| [`test_sistema_archivos.py`](test_sistema_archivos.py) | Contiene las pruebas automatizadas de `SistemaArchivos`. |
| [`Documentacion_Sistema_Archivos.docx`](Documentacion_Sistema_Archivos.docx) | Documentación editable del proyecto, organizada en las fases 1 a 5. |
| [`Documentacion_Sistema_Archivos.pdf`](Documentacion_Sistema_Archivos.pdf) | Versión en PDF de la documentación del proyecto. |
| [`Diagrama_UML_Sistema_Archivos.png`](Diagrama_UML_Sistema_Archivos.png) | Diagrama UML basado en las clases y dependencias reales del código. |

## Ejemplo del árbol

```text
Documentos
├── Apuntes
│   └── Agenda.txt
└── Proyectos
    └── Tarea.txt
```

El dibujo representa las relaciones entre los nodos del árbol binario simulado. Los archivos y directorios del ejemplo existen solo dentro del programa.

## Requisitos

- Python 3.
- Tkinter para la interfaz gráfica. Normalmente está incluido con Python.
- No es necesario instalar bibliotecas externas.

## Ejecutar la interfaz gráfica

Abre una terminal dentro de la carpeta del Proyecto 5 (`proyectos/05-arboles-sistema-archivos/`) y ejecuta:

```bash
python3 interfaz.py
```

## Ejecutar la versión de consola

Desde la misma carpeta, ejecuta:

```bash
python3 main.py
```

## Ejecutar las pruebas automatizadas

Desde la misma carpeta, ejecuta:

```bash
python3 -B -m unittest -v test_sistema_archivos.py
```

## Conceptos aplicados

- Clases y objetos.
- Árbol binario de búsqueda.
- Recursividad.
- Recorridos inorden, preorden y postorden.
- Validación de datos.
- Pruebas unitarias con `unittest`.
- Interfaces gráficas con Tkinter.
