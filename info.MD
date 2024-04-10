Rutas del API

- [POST] /search
Busca un producto o cliente en la base de datos segun un parametro de busqueda. **BUSQUEDA APROXIMADA**.
BODY:
```json
{
    "table": "product" | "client",
    "field": "pid" | "name" | "code"
    "value": string
}
```
- Si el field es `pid`, se busca por cedula en la tabla de clientes.
- Si el field es `name` y la tabla es `client`, se busca por `CONCAT(name, ' ', surname)`.
- Si el field es `name` y la tabla es `product`, se busca por nombre en la tabla de productos.
- Si el field es `code`, se busca por codigo en la tabla de productos.

RETURNS:

Si la tabla es `product`
```json
{
    "result": {
        "code": string,
        "name": string,
        "photourl": string,
        "price": number,
    }[]
}
```

Si la tabla es `client`

```json
{
    "result":{
        "dir": string,
        "id_client": number,
        "name": string,
        "pid": string,
        "pid_prefix": "V" | "E" | "J",
        "surname": "Santana"
    }[]
}
```

- [POST] /createClient

Crea o actualiza un cliente en la base de datos (basado en su `pid`).

Si el `pid` ya existe en la base de datos, se actualiza la informacion del cliente.

BODY:
```json
{
    "pid": "10000000",
    "pid_prefix": "E",
    "dir": "La Cañada",
    "name": "Pedro",
    "surname": "Urdaneta"
}
```

RETURNS:
```json
{
    "result": {
        "action": "update" | "insert",
        "client_id": number
    }
}
```

- [POST] /createInvoice

Crea una factura en la base de datos. Falla si la caja esta cerrada.

BODY:
```json
{
    "invoice": {
        "client": {
            "name": string,
            "surname": string,
            "pid": string,
            "pid_prefix": "V" | "E" | "J",
            "dir": string
        },
        "products": {
            "name": string,
            "code": string,
            "quantity": number
        }[],
        "payments": {
            "method": "EFECTIVO" | "TARJETA DE DEBITO" | "TARJETA DE CREDITO" | "ZELLE",
            "amount": number, 
            "bank": "BNC" | "VENEZUELA" | "BANESCO" | "BOFA" | "CHASE" | null,
        }[],

    }
}
```

RETURNS:

Si la caja esta abierta:
```json
{
    "result": {
        "message": "Invoice created successfully",
        "invoice_id": number,
        "insert": true
    }
}
```

Si la caja esta cerrada:
```json
{
    "result": {
        "message": "Closing already happened",
        "insert": false
    }
}
```

- [POST] /getInvoice

Devuelve la informacion completa de una factura segun su id:

BODY:
```json
{
    "invoice_id": number
}
```

RETURNS:
```json
{
    "result": {
        "client": {
            "dir": string,
            "name": string,
            "pid": string,
            "pid_prefix": "V" | "E" | "J",
            "surname": string
        },
        "date": "YYYY-MM-DD",
        "invoice_id": number,
        "payments": {
            "method": "EFECTIVO" | "TARJETA DE DEBITO" | "TARJETA DE CREDITO" | "ZELLE",
            "amount": number, 
            "bank": "BNC" | "VENEZUELA" | "BANESCO" | "BOFA" | "CHASE" | null,
        }[],
        "products":{
            "code": string,
            "name": string,
            "photourl": string,
            "price": number,
            "quantity": number
        }[],
        "void": true | false // si la factura fue anulada
    }
}
```

- [POST] /searchInvoice

Busca una factura el la base de datos segun un parametro. BUSCA CAMPOS REDUCIDOS.

PARAMETROS VALIDOS:
- `name`: Busca por `CONCAT(name, ' ', surname)` del cliente.
- `pid`: Busca por cedula del cliente.
- `invoice_id`: Busca por id de la factura.
- `date`: Busca por fecha de la factura (FORMATO YYYY-MM-DD).

BODY:
```json
{
    "field": "name" | "pid" | "invoice_id" | "date",
    "value": string
}
```

RETURNS:
```json
{
    "result": {
        "date": "YYYY-MM-DD",
        "invoice_id": number,
        "name": string,
        "pid": string,
        "pid_prefix": "V" | "E" | "J",
        "surname": string,
        "total": number,
        "void": true | false 
    }[]
}
```

- [POST] /voidInvoice

Anula una factura en la base de datos.

BODY:
```json
{
    "invoice_id": number
}
```

RETURNS:
```json
{
    "result": {
        "message": "Invoice voided successfully"
    }
}
```

- [POST] /getClosingStatement

Devuelve el estado de la caja en una fecha especifica.

BODY:
```json
{
    "date": "YYYY-MM-DD"
}
```

RETURNS:
```json
{
    "result": {
        "average_invoice": number,
        "banks": {
            "bank": "BNC" | "VENEZUELA" | "BANESCO" | "BOFA" | "CHASE" | "EFECTIVO",
            "total": number
        },
        "closing_time": "YYYY-MM-DD HH:MM:SS" | "",
        "date": "YYYY-MM-DD",
        "day_total": number,
        "invoice_quantity": number,
        "invoices": {
            "date": "YYYY-MM-DD",
            "invoice_id": number,
            "name": string,
            "pid": string,
            "pid_prefix": "V" | "E" | "J",
            "surname": string,
            "total": number,
            "void": true | false
        }[],
            
        "methods": 
        {
            "method": "EFECTIVO" | "TARJETA DE DEBITO" | "TARJETA DE CREDITO" | "ZELLE",
            "total": number
        }[],
            
        "products": {
            "name": string,
            "sold": number,
            "total": number
        }[],

    }
}
```

Si la caja no ha sido cerrada `closing_time` es un string vacio.

- [POST] /close

Cierra la caja en la base de datos.

NO LLEVA BODY.

RETURNS:

Si ya se cerro la caja:
```json
{
    "result": {
        "message": "Closing already happened",
        "insert": false
    }
}
```

Si se pudo cerrar la caja con exito:
```json
{
    "result": {
        "message": "Closing don successfully",
        "insert": true
    }
}
```


