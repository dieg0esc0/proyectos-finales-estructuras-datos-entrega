# Cola de Impresión

## Descripción

Este proyecto simula una cola de impresión compartida por cinco computadoras (PC1 a PC5). Los trabajos se guardan en una **cola (FIFO)** y se imprimen en el mismo orden en que llegaron: el primero que entra es el primero que se imprime.

## Funcionalidades

- Agregar un trabajo de impresión desde una PC elegida al azar (o presionando una PC).
- Imprimir el primer trabajo de la cola y mostrar qué computadora se está atendiendo.
- Mostrar la cola con todos los trabajos pendientes en orden de atención.
- Avisos "La cola de impresión está LLENA" (capacidad de 6) y "La cola de impresión está VACÍA".
- Ver el arreglo circular por dentro, con los índices frente y final.
- Lista de trabajos impresos y registro de cada encolar y desencolar.

## Estructura de archivos

| Archivo | Responsabilidad |
| --- | --- |
| [`cola_impresion.py`](cola_impresion.py) | Clases `Trabajo`, `Cola` (cola circular con arreglo), `ColaImpresion` y la interfaz gráfica con Tkinter. |
| [`Documentacion_Cola_Impresion.docx`](Documentacion_Cola_Impresion.docx) | Documentación del código. |

## Cómo ejecutarlo

```bash
python cola_impresion.py
```

Solo se necesita Python 3; Tkinter ya viene incluido.
