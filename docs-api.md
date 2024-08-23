# Documentación de la API

### Venta - crear una venta

`/api/v1/presupuesto/`

- **POST**:

  **_body_**

  ```json
  {
    "usuario": "Fede",
    "lote_cantidad": [
      { "lote": 1, "cantidad": 4 },
      { "lote": 2, "cantidad": 10 }
    ]
  }
  ```

  **_response_**

  HTTP Status Code: 201 Created ó 404 Bad Request

  ```json
  {
    "message": "Producto creado correctamente!",
    "data": {
      "venta_id": 36,
      "usuario": "Gusgus",
      "fecha": "2024-08-23T02:04:28.217459Z",
      "lote_cantidad": [
        {
          "cantidad": 1,
          "lote_id": 3,
          "nombre": "Freno Peugeot 201234",
          "precio_unitario": 999.0
        },
        {
          "cantidad": 1,
          "lote_id": 2,
          "nombre": "Freno Peugeot 201234",
          "precio_unitario": 18500.0
        }
      ]
    }
  }
  ```

### GET All Ventas - Trae todas las ventas

`/api/v1/gav/`

- **GET**:

  **_response_**

  ```json
  [
      {
          "venta_id": 1,
          "fecha": "2024-07-06T16:06:10.486355Z",
          "vendedor": "Empleado 2",
          "precio_total": 1500000.0,
          "lote_cantidad": [
              {
                  "lote_id": 1,
                  "descripcion": "Piston",
                  "precio_unitario": 150000.0,
                  "codigo_de_barra": "04684965",
                  "codigo_local": "fh32",
                  "cantidad": 4
              },
              {
                  "lote_id": 2,
                  "descripcion": "Freno Peugeot 2015",
                  "precio_unitario": 18500.0,
                  "codigo_de_barra": "00231548",
                  "codigo_local": "f78d",
                  "cantidad": 2
              }
          ]
      },
      {...},
      {...},
  ]
  ```

### Venta por ID - sólo info de la venta

`/api/v1/vget/36/`

- **GET**:

  **_response_**

  ```json
  {
    "venta_id": "36",
    "vendedor": "Gusgus",
    "fecha": "2024-08-23T02:04:28.217459Z",
    "venta": [
      {
        "tb_inter_id": 65,
        "venta_id": 36,
        "lote_id": 3,
        "descripcion": "Freno Peugeot 201234",
        "precio_unidad": 999.0,
        "codigo_de_barra": "45sd646",
        "cantidad_vendida": 1
      },
      {
        "tb_inter_id": 66,
        "venta_id": 36,
        "lote_id": 2,
        "descripcion": "Freno Peugeot 201234",
        "precio_unidad": 18500.0,
        "codigo_de_barra": "002w315g48",
        "cantidad_vendida": 1
      }
    ]
  }
  ```

### Ventas con Lotes y Proveedores

`/api/v1/ventas/`

- **_GET_**:

  **_response_**

  ```json
  [
    {
      "usuario": "Empleado 2",
      "fecha": "2024-07-06T16:06:10.486355Z",
      "precio_de_venta_total": "1500000.00",
      "lotes": [
        {
          "id": 2,
          "codigo_barra": "00231548",
          "precio_de_compra": "10000.00",
          "cantidad": 22,
          "precio_bonificado": "9500.00",
          "ultimo_precio": "9500.00",
          "proveedor": {
            "id": 2,
            "nombre": "Auto partes Mignol",
            "url": "www.mignolo.ar"
          },
          "precio_de_venta": "18500.00",
          "iva": "21.00"
        },
        {
          "id": 3,
          "codigo_barra": "45646",
          "precio_de_compra": "456.12",
          "cantidad": 99,
          "precio_bonificado": "456.12",
          "ultimo_precio": "354.10",
          "proveedor": {
            "id": 2,
            "nombre": "Auto partes Mignol",
            "url": "www.mignolo.ar"
          },
          "precio_de_venta": "999.00",
          "iva": "21.00"
        }
      ]
    },
    {...},
    {...},
  ]
  ```

`/api/v1/ventas/1/`

- **_GET_**:

  **_response_**

  ```json
  {
    "usuario": "Empleado 2",
    "fecha": "2024-07-06T16:06:10.486355Z",
    "precio_de_venta_total": "1500000.00",
    "lotes": [
      {
        "id": 2,
        "codigo_barra": "00231548",
        "precio_de_compra": "10000.00",
        "cantidad": 22,
        "precio_bonificado": "9500.00",
        "ultimo_precio": "9500.00",
        "proveedor": {
          "id": 2,
          "nombre": "Auto partes Mignol",
          "url": "www.mignolo.ar"
        },
        "precio_de_venta": "18500.00",
        "iva": "21.00"
      },
      {
        "id": 3,
        "codigo_barra": "45646",
        "precio_de_compra": "456.12",
        "cantidad": 99,
        "precio_bonificado": "456.12",
        "ultimo_precio": "354.10",
        "proveedor": {
          "id": 2,
          "nombre": "Auto partes Mignol",
          "url": "www.mignolo.ar"
        },
        "precio_de_venta": "999.00",
        "iva": "21.00"
      }
    ]
  }
  ```

### Productos - Lotes - proveedores

`/api/v1/plp/`

- **_GET_**:

  **_response_**

  ```json
  [
    {
      "id": 1,
      "descripcion": "Freno Peugeot 2015",
      "codigo_del_local": "f78d",
      "modelo": "Full",
      "marca": "Peugeot",
      "lote": [
        {
          "id": 2,
          "codigo_barra": "00231548",
          "precio_de_compra": "10000.00",
          "cantidad": 50,
          "precio_bonificado": "9500.00",
          "ultimo_precio": "9500.00",
          "proveedor": {
            "id": 2,
            "nombre": "Auto partes Mignolo",
            "url": "www.mignolo.com.ar"
          },
          "precio_de_venta": "18500.00",
          "iva": "21.00"
        }
      ]
    },
    {...},
    {...},
  ]
  ```

### Productos

`/api/v1/productos/`

- **_GET_**: Devuelve todos los productos

  **response**

  ```json
  [
    {
      "id": 1,
      "descripcion": "Freno Peugeot 2015",
      "codigo_del_local": "f78d",
      "modelo": "Full",
      "marca": "Peugeot"
    },
    {...},
    {...},
  ]
  ```

- **_POST_**: Carga un producto

  **body**

  ```json
  {
    "descripcion": "Freno Peugeot 2015",
    "codigo_del_local": "f78d",
    "modelo": "Full",
    "marca": "Peugeot"
  }
  ```

`/api/v1/productos/5/`

- **_GET_**: Devuelve un producto por ID

  **response**

  ```json
  {
    "id": 5,
    "descripcion": "Amortiguador",
    "codigo_del_local": "j337o",
    "modelo": "Rebotin",
    "marca": "Peugeot"
  }
  ```

- **_PUT ó PATCH + id_**: Modifica un producto por id ej => `/api/v1/productos/3/`

  **body**

  ```json
  {
    "descripcion": "Descrip. modificada",
    "codigo_del_local": "f78d",
    "modelo": "Full",
    "marca": "Peugeot"
  }
  ```

- **_DELETE + id_**: Elimina un producto por id ej => `/api/v1/productos/3/`

- (Si un producto se elimina, también se eliminan los lotes asociados aunque todavía haya stock, y también se eliminan los lotes de las tablas intermedias, rompiendo las relaciones, por la prop. **on_delete=models.CASCADE**, recomendación: no usar... o usar un eliminar lógico [activo/inactivo])

  **response**

Creo que no devuelve nada tampoco...

```json
{
  "descripcion": "Descrip. modificada",
  "codigo_del_local": "f78d",
  "modelo": "Full",
  "marca": "Peugeot"
}
```

### Productos {ID y descripción}

- (No usar POST, PUT, PATCH)

`/api/v1/productos-id-desc/`

- **_GET_**: Devuelve todos los productos (sólo id y descripción)

  **response**

  ```json
  [
    {
      "id": 1,
      "descripcion": "Freno Peugeot 201234"
    },
    {
      "id": 2,
      "descripcion": "Freno Nissan"
    },
    {...},
    {...},
  ]
  ```

`/api/v1/productos-id-desc/4/`

- **_GET_**: Devuelve un producto por ID (sólo id y descripción)

  **response**

  ```json
  {
    "id": 4,
    "descripcion": "Piston"
  }
  ```

`/api/v1/productos-id-desc/4/`

- **_DELETE_**: Elimina un producto por ID

No devuelve nada... Por ahora

### Productos {ID y código del local}

- (No usar POST, PUT, PATCH)

`/api/v1/productos-id-codigo/`

- **_GET_**: Devuelve todos los productos (sólo id y código del local)

  **response**

  ```json
  [
     {
        "id": 1,
        "codigo_local": "f78d"
    },
    {
        "id": 2,
        "codigo_local": "48s"
    },
    {...},
    {...},
  ]
  ```

`/api/v1/productos-id-codigo/4/`

- **_GET_**: Devuelve un producto por ID (sólo id y código del local)

  **response**

  ```json
  {
    "id": 4,
    "codigo_local": "fh32"
  }
  ```

`/api/v1/productos-id-codigo/`

- **_DELETE_**: Elimina un producto por ID

No devuelve nada... Por ahora

### Proveedores

`/api/v1/proveedores/`

- **_GET_**: Devuelve todos los proveedores

  **response**

  ```json
  [
    {
        "id": 1,
        "nombre": "Repuestos Warnes",
        "url": "www.re-warnes.com"
    },
    {...},
    {...},
  ]
  ```

- **_POST_**: Carga un proveedor

  **body**

  ```json
  {
    "nombre": "Repuestos Warnes",
    "url": "www.re-warnes.com"
  }
  ```

`/api/v1/proveedores/1/`

- **_GET_**: Devuelve un proveedor por ID

  **response**

  ```json
  {
    "id": 1,
    "nombre": "Repuestos Warnes",
    "url": "www.re-warnes.com"
  }
  ```

- **_PUT ó PATCH + id_**: Modifica un proveedor por id ej => `/api/v1/proveedores/1/`

  **body**

  ```json
  {
    "nombre": "Repuestos modificado",
    "url": "www.re-warnes.com"
  }
  ```

- **_DELETE + id_**: Elimina un proveedor por id ej => `/api/v1/proveedores/5/`

### Proveedores ID nombre {ID y nombre}

`/api/v1/proveedores-id-nombre/`

- **_GET_**: Devuelve todos los proveedores (sólo id y nombre)

  **response**

  ```json
  [
    {
        "id": 1,
        "nombre": "Repuestos Warnes"
    },
    {...},
    {...},
  ]
  ```

`/api/v1/proveedores-id-nombre/1/`

- **_GET_**: Devuelve un proveedor por ID (sólo id y nombre)

  **response**

  ```json
  {
    "id": 1,
    "nombre": "Repuestos Warnes"
  }
  ```

### Proveedores ID url {ID y url}

`/api/v1/proveedores-id-url/`

- **_GET_**: Devuelve todos los proveedores (sólo id y url)

  **response**

  ```json
  [
    {
        "id": 1,
        "url": "www.re-warnes.com"
    },
    {...},
    {...},
  ]
  ```

`/api/v1/proveedores-id-url/1/`

- **_GET_**: Devuelve un proveedor por ID (sólo id y url)

  **response**

  ```json
  {
    "id": 1,
    "url": "www.re-warnes.com"
  }
  ```

### Lotes

`/api/v1/lotes/`

- **_GET_**: Devuelve todos los lotes

  **response**

  ```json
  [
    {
        "id": 1,
        "codigo_barra": "0ad4684965",
        "fecha": "2024-07-03T20:07:19.632183Z",
        "precio_de_compra": "98000.00",
        "precio_bonificado": "95000.00",
        "ultimo_precio": "90000.00",
        "cantidad": 31,
        "precio_de_venta": "150000.00",
        "iva": "25.00",
        "proveedor": 1,
        "producto": 4
    },
    {...},
    {...},
  ]
  ```

- **_POST_**: Carga un lote

- (Antes de cargar un Lote debe existi el proveedor y el producto)

  **body**

  ```json
  {
    "codigo_barra": "45sd646",
    "precio_de_compra": 456.12,
    "precio_bonificado": 456.08,
    "ultimo_precio": 354.1,
    "cantidad": 100,
    "precio_de_venta": 999.0,
    "iva": 21,
    "proveedor": 1,
    "producto": 4
  }
  ```

`/api/v1/lotes/5/`

- **_GET_**: Devuelve un lote por ID

  **response**

  ```json
  {
    "id": 3,
    "codigo_barra": "45sd646",
    "fecha": "2024-08-23T01:46:13.376613Z",
    "precio_de_compra": 456.12,
    "precio_bonificado": 456.12,
    "ultimo_precio": 354.1,
    "cantidad": 100,
    "precio_de_venta": 999.0,
    "iva": 21.0,
    "proveedor": 1,
    "producto": 4
  }
  ```

- **_PUT ó PATCH + id_**: Modifica un lote por id ej => `/api/v1/lotes/3/`

  **body**

  ```json
  {
    "codigo_barra": "modificado",
    "fecha": "2024-08-23T01:46:13.376613Z",
    "precio_de_compra": 456.12,
    "precio_bonificado": 456.12,
    "ultimo_precio": 354.1,
    "cantidad": 100,
    "precio_de_venta": 999.0,
    "iva": 21.0,
    "proveedor": 1,
    "producto": 4
  }
  ```

- **_DELETE + id_**: Elimina un lote por id ej => `/api/v1/lotes/3/`

  **response**

Creo que no devuelve nada tampoco...
