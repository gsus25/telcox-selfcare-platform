# API Documentation

Documentacion de la API REST del modulo de visualizacion de consumo de TelcoX Selfcare Platform.

## Base URL

En ambiente local con Docker Compose:

```txt
http://localhost:5001
```

El backend corre internamente en el contenedor por el puerto `5000`, pero se expone al host en el puerto `5001`.

## Formato de respuesta

La API responde en formato JSON.

```http
Content-Type: application/json
```

## Endpoints

### Health Check

Permite validar que el backend esta levantado.

```http
GET /api/health
```

URL local:

```txt
http://localhost:5001/api/health
```

#### Respuesta exitosa

Status:

```txt
200 OK
```

Body:

```json
{
  "status": "ok"
}
```

## Consulta de consumo del cliente

Obtiene el saldo, consumo de datos, consumo de minutos y fecha de ultima actualizacion de un cliente.

```http
GET /api/customers/{customerId}/usage
```

### Parametros de ruta

| Parametro | Tipo | Requerido | Descripcion |
|---|---|---:|---|
| `customerId` | string | Si | Identificador del cliente en el sistema BSS/CRM simulado. |

### Clientes demo disponibles

| Customer ID | Nombre |
|---|---|
| `1001` | Ana Torres |
| `1002` | Carlos Mejia |

### Ejemplo de request

```txt
http://localhost:5001/api/customers/1001/usage
```

### Respuesta exitosa

Status:

```txt
200 OK
```

Body:

```json
{
  "balance": 18.75,
  "customerId": "1001",
  "customerName": "Ana Torres",
  "dataUsage": {
    "percentage": 36,
    "total": 20.0,
    "unit": "GB",
    "used": 7.2
  },
  "lastUpdated": "2026-06-19T16:30:00+00:00",
  "minutesUsage": {
    "percentage": 32,
    "total": 1000,
    "unit": "minutes",
    "used": 320
  }
}
```

### Campos de respuesta

| Campo | Tipo | Descripcion |
|---|---|---|
| `customerId` | string | Identificador del cliente. |
| `customerName` | string | Nombre del cliente. |
| `balance` | number | Saldo disponible del cliente. |
| `dataUsage.used` | number | Datos consumidos. |
| `dataUsage.total` | number | Total de datos disponibles. |
| `dataUsage.unit` | string | Unidad del paquete de datos. |
| `dataUsage.percentage` | number | Porcentaje de datos consumidos. |
| `minutesUsage.used` | number | Minutos consumidos. |
| `minutesUsage.total` | number | Total de minutos disponibles. |
| `minutesUsage.unit` | string | Unidad del paquete de minutos. |
| `minutesUsage.percentage` | number | Porcentaje de minutos consumidos. |
| `lastUpdated` | string | Fecha de ultima actualizacion en formato ISO 8601. |

## Errores

La API devuelve errores estructurados con los campos:

```json
{
  "error": "codigo_del_error",
  "message": "Mensaje legible para el usuario o consumidor de API."
}
```

### Cliente no encontrado

Ocurre cuando el `customerId` no existe en el BSS/CRM simulado.

Request:

```txt
http://localhost:5001/api/customers/9999/usage
```

Status:

```txt
404 Not Found
```

Body:

```json
{
  "error": "customer_not_found",
  "message": "No encontramos informacion de consumo para este cliente."
}
```

### BSS no disponible

Ocurre cuando el backend no puede consultar la fuente de datos del BSS/CRM simulado, por ejemplo si MySQL no esta disponible.

Status:

```txt
503 Service Unavailable
```

Body:

```json
{
  "error": "bss_unavailable",
  "message": "El sistema BSS no esta disponible temporalmente."
}
```

### Error interno

Ocurre ante un error inesperado del backend.

Status:

```txt
500 Internal Server Error
```

Body:

```json
{
  "error": "internal_server_error",
  "message": "No pudimos consultar el consumo en este momento."
}
```

## Como probar la API

Con los servicios levantados:

```bash
docker compose up --build
```

Probar health check:

```bash
curl http://localhost:5001/api/health
```

Probar cliente exitoso:

```bash
curl http://localhost:5001/api/customers/1001/usage
```

Probar segundo cliente:

```bash
curl http://localhost:5001/api/customers/1002/usage
```

Probar cliente inexistente:

```bash
curl http://localhost:5001/api/customers/9999/usage
```

## Relacion con el frontend

El frontend Angular consume el endpoint:

```txt
GET http://localhost:5001/api/customers/1001/usage
```

Actualmente el `customerId` se mantiene fijo como `1001` para simular un usuario autenticado.

En una version productiva, este identificador deberia provenir de:

- Sesion autenticada.
- Token JWT.
- Perfil de usuario del CRM.
- Seleccion de linea asociada a la cuenta.
