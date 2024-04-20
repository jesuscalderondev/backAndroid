# financiApp

## ENDPOINTS

### /login

Method: **POST**

- Body
```json
{
    "email": "user@mail.com",
    "password": "myPassword"
}
```

- Headers

```json
{   
    "Content-Type" : "application/json"
}
```

- Response
En el espacio de **token** debe ir un token de autenticación

```json
{   
    "token" : "<token>",
}
```

<hr>

### /register

El campo **term** se refiere al termino de días en los que transcurre el presupuesto, ejemplo 15 o 30 días.

Method: **POST**

- Body
```json
{
    "email": "user@mail.com",
    "password": "myPassword",
    "first_name": "William",
    "last_name": "Jordan",
    "budget": 1600000,
    "term": 30
}
```

- Headers

```json
{   
    "Content-Type" : "application/json"
}
```

- Response
En el espacio de **token** debe ir un token de autenticación

- - Caso de éxito
```json
{   
    "token" : "<token>",
}
```

<hr>

### /users/createTransaction

El campo **type** se refiere al movimiento, este puede ser *payment* para referirce a un pago, gasto, etc o *entry* que se refiere a un ingreso.

Method: **POST**

- Body
```json
{
    "amount" : 40000,
    "type" : "payment",
    "name" : "Pay services",
    "description" : "My description"
}
```


- Headers

En el espacio de **token** debe ir un token de autenticación

```json
{   
    "Authorization" : "Bearer <token>",
    "Content-Type" : "application/json"
}
```

- Response 

```json
{
    "message": "Se a registrado de manera exitosa su transacción"
}

```

<hr>

### /users/getTransactions/[month]/[year]

En la url se debe incluir el mes y el año en que se desean consultar las trancacciones, si es un mes menor a 10 debe incluirsde el 0 por delante, algo como Enero = 01, el año debe ser de 4 dígitos, es decir 2024 por ejemplo.

Method: **GET**


- Headers

En el espacio de **token** debe ir un token de autenticación

```json
{   
    "Authorization" : "Bearer <token>",
    "Content-Type" : "application/json"
}
```

- Response

```json
{
    "response": {
        "0": {
            "amount": 40000.0,
            "budget_id": "b65a65ff-2a7e-4d7d-96bc-17367752395c",
            "date": "Thu, 18 Apr 2024 19:40:14 GMT",
            "description": "Nada",
            "entry": true,
            "id": "16a82b78-d8d1-4bfe-b711-4385a6a2e42a",
            "name": "Pago de servicios"
        }
    }
}
```

<hr>

### /users/getData

Method: **GET**


- Headers

En el espacio de **token** debe ir un token de autenticación

```json
{   
    "Authorization" : "Bearer <token>",
    "Content-Type" : "application/json"
}
```
- Response

```json
{
    "response": {
        "default_budget": 1600000.0,
        "email": "user@mail.com",
        "first_name": "William",
        "last_name": "Jordan",
        "term": 30
    }
}
```

### /users/getBudgetNow

Method: **GET**


- Headers

En el espacio de **token** debe ir un token de autenticación

```json
{   
    "Authorization" : "Bearer <token>",
    "Content-Type" : "application/json"
}
```
- Response

```json
{
    "budget": 41783.0,
    "end": "Mon, 20 May 2024 00:00:00 GMT",
    "id": "0f38d4ac-ee6f-4d04-b07d-3c79843a0117",
    "start": "Sat, 20 Apr 2024 00:00:00 GMT",
    "transactions": [
        {
            "amount": 40000.0,
            "date": "Sat, 20 Apr 2024 05:40:49 GMT",
            "description": "Nada",
            "entry": true,
            "id": "1f808abc-6f85-4362-8377-acf52b56282e",
            "name": "Pago de servicios"
        },
        {
            "amount": 3000.0,
            "date": "Sat, 20 Apr 2024 05:42:33 GMT",
            "description": "Nada",
            "entry": true,
            "id": "fd06ffe3-9b99-430d-a912-255ea904dda1",
            "name": "Pago de alquiler"
        },
        {
            "amount": 3000.0,
            "date": "Sat, 20 Apr 2024 05:43:30 GMT",
            "description": "Nada",
            "entry": false,
            "id": "d2bb0cba-41a7-4eb9-9005-15ef4b963243",
            "name": "Pago de alimentación"
        }
    ],
    "user_id": "c5e6d3c4-ddcc-49aa-af59-12afef59b832"
}
```


### Errores

```json
{
    "error": "<Código de error>",
    "message": "<Mensaje del error>"
}
```