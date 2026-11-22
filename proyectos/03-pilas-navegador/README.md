# Navegador Web con Pilas

## Descripción

Este proyecto simula el funcionamiento básico de un navegador web. Usa dos pilas (LIFO) para guardar el historial de navegación: la **pila atrás** guarda las páginas visitadas antes de la actual y la **pila adelante** guarda las páginas a las que se puede volver después de usar Back.

## Funcionalidades

- Visitar una página escribiendo su URL (botón Visitar o tecla Enter).
- Regresar a la página anterior con Back y avanzar con Forward.
- Mostrar la página actual en todo momento.
- Limpiar la pila adelante al visitar una página nueva.
- Avisos de PILA VACÍA y PILA LLENA sin que el programa truene (capacidad de 4 páginas por pila).
- Validar la URL y agregar `https://` si no lo tiene.
- Dibujar las dos pilas y un registro de cada push y pop.
- Salir con Exit, con confirmación.

## Estructura de archivos

| Archivo | Responsabilidad |
| --- | --- |
| [`pila.py`](pila.py) | Clases `Nodo` y `Pila` (pila con nodos enlazados). |
| [`urls.py`](urls.py) | Validación y limpieza de URLs y descripción de cada página. |
| [`navegador.py`](navegador.py) | Clase `Navegador` con las dos pilas y los métodos visitar, retroceder y avanzar. |
| [`ventana.py`](ventana.py) | Interfaz gráfica con Tkinter. |
| [`main.py`](main.py) | Abre el programa. |
| [`pruebas.py`](pruebas.py) | 39 pruebas automáticas. |
| [`Documentacion_Navegador_Web.docx`](Documentacion_Navegador_Web.docx) | Documentación del código. |
| [`Auditoria_Avance_Proyecto_3_Navegador_Web.pdf`](Auditoria_Avance_Proyecto_3_Navegador_Web.pdf) | Auditoría de avance del proyecto. |

## Cómo ejecutarlo

```bash
python main.py
```

```bash
python pruebas.py
```

Solo se necesita Python 3; Tkinter ya viene incluido.
