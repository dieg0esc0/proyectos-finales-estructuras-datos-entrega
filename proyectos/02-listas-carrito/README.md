# Carrito de Compras con Listas Enlazadas

## Descripción

Este proyecto simula el carrito de compras de una tienda en la consola. Toda la información se guarda en memoria usando listas enlazadas simples, como la vista en clase: el catálogo es una lista de productos y el carrito es una lista de renglones con el producto y la cantidad.

## Funcionalidades

- Mostrar un catálogo precargado de 10 productos con ID, nombre y precio.
- Buscar productos por ID o por nombre, sin distinguir mayúsculas y minúsculas.
- Agregar productos al carrito indicando la cantidad.
- Ver el carrito con cantidad, precio unitario, subtotal y total acumulado.
- Modificar la cantidad de un producto y actualizar el subtotal automáticamente.
- Eliminar productos por ID o por nombre.
- Vaciar el carrito y reiniciar la compra.
- Finalizar la compra mostrando los productos, el total de artículos y el monto a pagar.
- Validar las entradas del usuario.
- Ejecutar pruebas automatizadas con `unittest`.

## Reglas del carrito

- Cada nodo de la lista guarda un dato y la referencia al siguiente nodo. El último nodo apunta a `None`.
- Los productos nuevos se insertan al final de la lista del carrito.
- Si se agrega un producto que ya está en el carrito, se suma la cantidad en lugar de repetirlo.
- El subtotal no se guarda: se calcula como precio × cantidad, por eso se actualiza solo.
- Al eliminar un producto se liga el nodo anterior con el siguiente.
- Al finalizar la compra se muestra el ticket y el carrito queda vacío.

## Estructura de archivos

| Archivo | Responsabilidad |
| --- | --- |
| [`lista.py`](lista.py) | Define la lista enlazada: `NodoLista`, `Lista` y `ExcepcionListaVacia`. |
| [`carrito.py`](carrito.py) | Contiene las clases `Producto`, `ItemCarrito`, `Catalogo` y `Carrito`. |
| [`main.py`](main.py) | Proporciona el menú de consola (clase `Tienda`). |
| [`test_carrito.py`](test_carrito.py) | Contiene las pruebas automatizadas de la lista y del carrito. |
| [`Documentacion_Carrito_Compras.docx`](Documentacion_Carrito_Compras.docx) | Documentación del proyecto. |

## Ejemplo del carrito

```text
primerNodo                                          ultimoNodo
    │                                                    │
    ▼                                                    ▼
[Mouse x5] ──► [Memoria USB x1] ──► [Laptop x1] ──► None
```

Al eliminar la Memoria USB, el nodo del Mouse pasa a apuntar directamente al de la Laptop.

## Requisitos

- Python 3.
- No es necesario instalar bibliotecas externas.

## Ejecutar la versión de consola

Abre una terminal dentro de la carpeta del Proyecto 2 (`proyectos/02-listas-carrito/`) y ejecuta:

```bash
python3 main.py
```

## Ejecutar las pruebas automatizadas

Desde la misma carpeta, ejecuta:

```bash
python3 -B -m unittest -v test_carrito.py
```

## Conceptos aplicados

- Clases y objetos.
- Listas enlazadas simples.
- Inserción, búsqueda, actualización y eliminación de nodos.
- Excepciones.
- Validación de datos.
- Pruebas unitarias con `unittest`.
