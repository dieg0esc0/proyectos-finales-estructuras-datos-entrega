# Resistencia Eléctrica con Arreglos

## Descripción

Este proyecto usa arreglos para trabajar con resistencias eléctricas. A partir del valor de una resistencia en ohmios obtiene los colores de sus bandas y los dibuja en una ventana. También calcula la resistencia total de `n` resistencias conectadas en serie y en paralelo, donde cada resistor es un número entero aleatorio entre 10 y 1,000,000,000 Ω.

## Funcionalidades

- Obtener los colores de una resistencia a partir de su valor, incluyendo valores con decimales (4.7 Ω, 0.47 Ω).
- Dibujar la resistencia con cada banda pintada de su color.
- Generar `n` resistores aleatorios entre 10 y 1,000,000,000 Ω.
- Calcular la resistencia total en serie.
- Calcular la suma de inversos (resultado intermedio) y la resistencia total en paralelo en ohmios.
- Validar el valor de la resistencia y la cantidad `n`.
- Usar un menú de consola o una interfaz gráfica con Tkinter.
- Ejecutar pruebas automatizadas con `unittest`.

## Reglas de los colores

- La resistencia tiene 3 bandas: la primera es el primer dígito, la segunda es el segundo dígito y la tercera es el multiplicador.
- El color del multiplicador es la cantidad de ceros que siguen. Por ejemplo, 5800 tiene 2 ceros, así que el multiplicador es `COLORES[2]` = Rojo (×100).
- Después de los dos primeros dígitos solo puede haber ceros. Un valor como 165 no se puede representar con 3 bandas.
- Para valores de 1 a 9.9 Ω el multiplicador es Dorado (×0.1) y para valores de 0.1 a 0.99 Ω es Plateado (×0.01).
- Serie: `Rts = R1 + R2 + … + Rn`.
- Paralelo: el PDF escribe solo la suma `1/R1 + 1/R2 + … + 1/Rn`, que es un resultado intermedio (en siemens). La resistencia en ohmios es `Rtp = 1 / (1/R1 + 1/R2 + … + 1/Rn)`. El programa muestra los dos valores.

## Estructura de archivos

| Archivo | Responsabilidad |
| --- | --- |
| [`resistencia.py`](resistencia.py) | Contiene los arreglos de la tabla de colores y las clases `Resistencia` (colores) y `Circuito` (serie y paralelo). |
| [`main.py`](main.py) | Proporciona el menú de consola. |
| [`interfaz.py`](interfaz.py) | Proporciona la interfaz gráfica con Tkinter y dibuja la resistencia. |
| [`test_resistencia.py`](test_resistencia.py) | Contiene las pruebas automatizadas de `Resistencia` y `Circuito`. |
| [`Documentacion_Resistencia.docx`](Documentacion_Resistencia.docx) | Documentación del proyecto (Fases 1 a 5). |

## Ejemplo de colores

| Valor | Colores |
| --- | --- |
| 160 Ω | Marrón, Azul, Marrón |
| 5800 Ω | Verde, Gris, Rojo |
| 47000 Ω | Amarillo, Violeta, Naranja |
| 1,000,000,000 Ω | Marrón, Negro, Gris |
| 1 Ω | Marrón, Negro, Dorado |
| 4.7 Ω | Amarillo, Violeta, Dorado |
| 0.47 Ω | Amarillo, Violeta, Plateado |

Los dos primeros ejemplos son los que pide el proyecto.

## Requisitos

- Python 3.
- Tkinter para la interfaz gráfica. Normalmente está incluido con Python.
- No es necesario instalar bibliotecas externas.

## Ejecutar la interfaz gráfica

Abre una terminal dentro de la carpeta del Proyecto 1 (`proyectos/01-arreglos-resistencia/`) y ejecuta:

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
python3 -B -m unittest -v test_resistencia.py
```

## Conceptos aplicados

- Clases y objetos.
- Arreglos unidimensionales.
- Recorrido de arreglos con ciclos e índices.
- Números aleatorios.
- Validación de datos.
- Pruebas unitarias con `unittest`.
- Interfaces gráficas con Tkinter.
