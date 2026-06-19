# API Documentation

Documentacion de la API REST del modulo de visualizacion de consumo de TelcoX Selfcare Platform.

## Base URL

En ambiente local con Docker Compose: http://localhost:5001
*(El backend corre internamente en el contenedor por el puerto 5000, pero se expone al host en el puerto 5001).*

## Formato de Respuesta
Todas las respuestas de la API utilizan formato JSON (Content-Type: application/json).

---

## Endpoints

### 1. Health Check
Valida el estado del servicio backend.

- URL: GET /api/health
- Response (200 OK):

```json
{
  "status": "ok"
}
```

### 2. Consulta de Consumo del Cliente
Obtiene el saldo, consumo de datos, consumo de minutos y fecha de ultima actualizacion.

- URL: GET /api/customers/{customerId}/usage
- Path Parameters:
  - customerId (string, requerido): Identificador del cliente.

Clientes demo disponibles:
- 1001 - Ana Torres
- 1002 - Carlos Mejia

#### Respuesta Exitosa (200 OK)
*Nota: Los valores numericos de consumo (balance, total, used) se manejan con un maximo de 2 decimales para precision en UI.*

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

#### Respuestas de Error
La API devuelve errores estructurados para facilitar su manejo en el frontend.

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

---

## Pruebas Manuales (cURL)

Con el entorno Docker en ejecucion, puedes validar los endpoints rapidamente:

### Health check

```bash
curl http://localhost:5001/api/health
```

### Cliente exitoso

```bash
curl http://localhost:5001/api/customers/1001/usage
```

### Cliente inexistente

```bash
curl http://localhost:5001/api/customers/9999/usage
```

