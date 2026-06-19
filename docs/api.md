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
{
  "status": "ok"
}

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

{
  "customerId": "1001",
  "customerName": "Ana Torres",
  "balance": 18.75,
  "dataUsage": {
    "used": 7.20,
    "total": 20.00,
    "unit": "GB",
    "percentage": 36
  },
  "minutesUsage": {
    "used": 320,
    "total": 1000,
    "unit": "minutes",
    "percentage": 32
  },
  "lastUpdated": "2026-06-19T16:30:00+00:00"
}

#### Respuestas de Error
La API devuelve errores estructurados para facilitar su manejo en el frontend.

404 Not Found (Cliente inexistente)
{
  "error": "customer_not_found",
  "message": "No encontramos informacion de consumo para este cliente."
}

503 Service Unavailable (BSS/MySQL caido)
{
  "error": "bss_unavailable",
  "message": "El sistema BSS no esta disponible temporalmente."
}

500 Internal Server Error
{
  "error": "internal_server_error",
  "message": "No pudimos consultar el consumo en este momento."
}

---

## Pruebas Manuales (cURL)

Con el entorno Docker en ejecucion, puedes validar los endpoints rapidamente:

# Health check
curl http://localhost:5001/api/health

# Cliente exitoso
curl http://localhost:5001/api/customers/1001/usage

# Cliente inexistente
curl http://localhost:5001/api/customers/9999/usage
