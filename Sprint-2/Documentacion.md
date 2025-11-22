# Documentación del Proyecto Tienda_Aurelion con Dashboard de Análisis de Ventas

## 1. Introducción
Este proyecto procesa datos comerciales de una tienda minorista para generar inteligencia de negocios (BI). El script de Python integra múltiples fuentes de datos dispersas (clientes, productos, ventas) para responder preguntas clave sobre el rendimiento del negocio.

## 2. Fuentes de Datos (Input)
El sistema utiliza cuatro archivos xlsx interrelacionados:

| Archivo | Contenido | Clave Primaria/Foránea |
| :--- | :--- | :--- |
| `clientes.xlsx` | Información demográfica de los compradores. | PK: `id_cliente` |
| `productos.xlsx` | Catálogo de artículos y precios base. | PK: `id_producto` |
| `ventas.xlsx` | Cabecera de las transacciones (fecha, cliente). | PK: `id_venta`, FK: `id_cliente` |
| `detalle_ventas.xlsx` | Renglones de cada factura (qué items se llevaron). | FK: `id_venta`, FK: `id_producto` |

## 2.1. Esquema de Relaciones (Modelo de Datos)

La estructura de la base de datos sigue un esquema de estrella simplificado, donde las ventas y sus detalles actúan como tablas de hechos y los clientes/productos como dimensiones.

 CLIENTES ||--o{ VENTAS : "Realiza (1 a N)"
    VENTAS ||--|{ DETALLE_VENTAS : "Contiene (1 a N)"
    PRODUCTOS ||--o{ DETALLE_VENTAS : "Se lista en (1 a N)"

    CLIENTES {
        int id_cliente PK
        string nombre
        string ciudad
    }

    VENTAS {
        int id_venta PK
        date fecha
        int id_cliente FK
    }

    DETALLE_VENTAS {
        int id_venta FK
        int id_producto FK
        int cantidad
        float importe
    }

    PRODUCTOS {
        int id_producto PK
        string nombre
        float precio
    }

## 3. Metodología de Procesamiento (ETL)

### 3.1 Extracción y Limpieza
Se utilizan funciones de `pandas` para la lectura. Se detectó que los archivos tienen extensiones (`xlsx`) y se ajustó la ruta de carga acorde.

### 3.2 Transformación y Fusión (Fix Crítico)
El desafío principal fue la unificación de tablas (**Data Merging**).
* **Problema Detectado:** Las tablas `detalle_ventas` y `productos` comparten la columna `nombre_producto`. Al hacer un `merge` estándar, Pandas renombra estas columnas a `nombre_producto_x` y `nombre_producto_y`.
* **Solución Aplicada:** Se utilizó el parámetro `suffixes=('', '_dup')` en la función `pd.merge`.
    * Esto fuerza a Pandas a mantener el nombre original (`nombre_producto`) para la columna de la tabla izquierda (Detalle).
    * La columna duplicada de la derecha (Productos) se renombra a `nombre_producto_dup`, evitando conflictos y permitiendo agrupaciones limpias.

## 4. Análisis Realizados

### Tarea 1: Análisis de Producto
Se generan dos rankings utilizando agregaciones `sum()`:
1.  **Volumen:** Productos con mayor `cantidad` vendida.
2.  **Facturación:** Productos con mayor `importe` total acumulado.
Esto permite diferenciar productos populares ("ganchos") de productos rentables ("vacas lecheras").

### Tarea 2: Análisis Temporal
Se convierte el campo `fecha` a formato `datetime` y se agrupa por periodo mensual (`dt.to_period('M')`).
* **Objetivo:** Visualizar la tendencia de ingresos para detectar estacionalidad o crecimiento.

### Tarea 3: Análisis de Clientes (Pareto)
Se agrupan las ventas por `nombre_cliente` sumando el `importe`.
* **Objetivo:** Identificar a los "Top 5" clientes que representan la mayor parte de los ingresos (Clientes VIP).

## 5. Requisitos para Ejecución
* Python 3.8+
* Librerías: `pandas`, `matplotlib`, `seaborn`
* Los archivos xlsx deben estar en el mismo directorio que el notebook.