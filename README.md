# financiApp

## ENDPOINTS

### /register

El campo <b>term</b> se refiere al termino de días en los que transcurre el presupuesto, ejemplo 15 o 30 días.

Method: <b>POST</b>

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

En el espacio de <b>token</b> debe ir un token de autenticación

```json
{   
    "Content-Type" : "application/json"
}
```

<hr>

### /users/createTransaction

El campo <b>type</b> se refiere al movimiento, este puede ser *payment* para referirce a un pago, gasto, etc o *entry* que se refiere a un ingreso.

Method: <b>POST</b>

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

En el espacio de <b>token</b> debe ir un token de autenticación

```json
{   
    "Authorization" : "Bearer <token>",
    "Content-Type" : "application/json"
}
```

<hr>

### /users/getTransactions/[month]/[year]

En la url se debe incluir el mes y el año en que se desean consultar las trancacciones, si es un mes menor a 10 debe incluirsde el 0 por delante, algo como Enero = 01, el año debe ser de 4 dígitos, es decir 2024 por ejemplo.

Method: <b>GET</b>


- Headers

En el espacio de <b>token</b> debe ir un token de autenticación

```json
{   
    "Authorization" : "Bearer <token>",
    "Content-Type" : "application/json"
}
```

<hr>