# Ruta Mágica — Grafo de Pueblos Mágicos de Yucatán

## Descripción

Ruta Mágica calcula el camino más corto entre dos pueblos del conjunto de datos. Representa siete pueblos y diez carreteras mediante un grafo ponderado no dirigido.

## Funcionalidades

- Cargar los pueblos y las carreteras desde archivos de texto.
- Mostrar un mapa esquemático con los nombres y las distancias.
- Seleccionar el origen y el destino en listas desplegables.
- Calcular la ruta más corta con Dijkstra y resaltar sus carreteras en rojo.
- Mostrar cada tramo, el camino completo y la distancia total.
- Consultar la matriz de adyacencia y limpiar la selección para buscar otra ruta.

## Reglas del grafo

- Cada pueblo es un vértice y cada carretera directa es una arista con un peso en kilómetros.
- Las carreteras son bidireccionales.
- En la matriz, la diagonal contiene 0 y el símbolo ∞ indica que no hay carretera directa.
- La interfaz requiere dos pueblos distintos para calcular una ruta.

## Estructura de archivos

| Archivo | Responsabilidad |
| --- | --- |
| [`pueblo.py`](pueblo.py) | Define el vértice con nombre y posición en el mapa. |
| [`carretera.py`](carretera.py) | Guarda el destino y los kilómetros de una conexión. |
| [`grafo.py`](grafo.py) | Carga los datos, mantiene las listas de adyacencia y consulta conexiones directas. |
| [`ruta.py`](ruta.py) | Representa el camino, los tramos y la distancia total. |
| [`dijkstra.py`](dijkstra.py) | Selecciona vértices, actualiza distancias y reconstruye el camino. |
| [`ventana.py`](ventana.py) | Muestra el mapa, los controles, el resultado y la matriz en Tkinter. |
| [`main.py`](main.py) | Localiza los datos, carga el grafo e inicia la interfaz. |
| [`pueblos.txt`](pueblos.txt) | Contiene los nombres y las coordenadas de los siete pueblos. |
| [`carreteras.txt`](carreteras.txt) | Contiene las diez conexiones y sus distancias en kilómetros. |

## Ejemplo de una ruta

Sisal → Motul → Izamal → Valladolid suma **245 km**. Los tramos recorren 96 km, 39 km y 110 km, respectivamente.

## Requisitos

- Python 3.
- Tkinter, incluido en las distribuciones de Python que lo habilitan.
- Los archivos de datos deben estar en la misma carpeta que el programa.

## Ejecutar la interfaz gráfica

Desde la carpeta del proyecto, ejecuta

~~~bash
python main.py
~~~

## Pruebas realizadas

Se comprobó el inicio, las rutas Sisal–Valladolid (245 km), Tekax–Espita (218 km) y Maní–Motul (153 km), los avisos de selección, el botón Limpiar y la matriz. Se usaron comprobaciones temporales y capturas de la aplicación. El informe académico está disponible en [DOCX](Documentacion_Proyecto_6.docx) y [PDF](Documentacion_Proyecto_6.pdf).

## Conceptos aplicados

- Vértices, aristas y pesos en un grafo no dirigido.
- Listas de adyacencia para guardar conexiones y una matriz para consultarlas.
- Dijkstra selecciona el pueblo pendiente de menor distancia conocida y actualiza sus vecinos. Los predecesores guardados permiten reconstruir el camino.
- Clases de Python e interfaz gráfica con Tkinter.
