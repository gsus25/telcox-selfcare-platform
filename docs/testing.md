# Testing Documentation

Documentacion de pruebas para TelcoX Selfcare Platform.

## Objetivo

Validar que el modulo de visualizacion de consumo funciona correctamente desde backend, API, base de datos y frontend.

El alcance de pruebas cubre:

- Health check del backend.
- Consulta exitosa de consumo.
- Cliente inexistente.
- BSS/MySQL no disponible.
- Servicio HTTP del frontend.
- Componente principal del dashboard.
- Visualizacion de errores amigables en la interfaz.

## Pruebas automatizadas

El proyecto incluye pruebas automatizadas en backend y frontend.

Backend:

```txt
backend/tests/test_usage.py
```

Frontend:

```txt
frontend/src/app/app.component.spec.ts
frontend/src/app/features/usage/services/usage-api.service.spec.ts
frontend/src/app/features/usage/pages/usage-dashboard/usage-dashboard.component.spec.ts
```

## Ejecutar pruebas backend

Desde la raiz del proyecto:

```bash
docker compose run --rm backend pytest
```

Resultado esperado:

```txt
4 passed
```

## Casos cubiertos por tests backend

### 1. Health check

Valida que el backend responda correctamente.

Endpoint:

```http
GET /api/health
```

Resultado esperado:

```json
{
  "status": "ok"
}
```

### 2. Consulta exitosa de consumo

Valida que la API devuelva el contrato esperado para un cliente existente.

Endpoint:

```http
GET /api/customers/1001/usage
```

Aspectos verificados:

- Status HTTP `200`.
- `customerId`.
- `customerName`.
- `balance`.
- Porcentaje de consumo de datos.
- Porcentaje de consumo de minutos.
- Campo `lastUpdated`.

### 3. Cliente inexistente

Valida que la API responda correctamente cuando el cliente no existe.

Endpoint:

```http
GET /api/customers/9999/usage
```

Resultado esperado:

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

### 4. BSS no disponible

Valida que la API maneje correctamente una falla en la fuente de datos.

Resultado esperado:

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

## Por que los tests backend mockean el BSS

Los tests unitarios de API no dependen de MySQL directamente. En su lugar, simulan el comportamiento del servicio BSS usando `monkeypatch`.

Esto permite probar la logica HTTP de forma rapida y estable:

- Caso exitoso.
- Error de cliente inexistente.
- Error de BSS no disponible.

La integracion real con MySQL se valida levantando el stack completo con Docker Compose.

## Ejecutar pruebas frontend

Desde la carpeta `frontend`:

```bash
cd frontend
npm test -- --watch=false --browsers=ChromeHeadless
```

Resultado esperado:

```txt
TOTAL: 3 SUCCESS
```

## Casos cubiertos por tests frontend

### 1. App shell

Valida que el componente principal de Angular se cree correctamente y renderice el dashboard.

Archivo:

```txt
frontend/src/app/app.component.spec.ts
```

### 2. UsageApiService

Valida que el servicio Angular haga una peticion `GET` al endpoint correcto:

```txt
http://localhost:5001/api/customers/1001/usage
```

Tambien valida que el payload recibido conserve los campos principales del modulo de consumo:

- Nombre del cliente.
- Saldo.
- Porcentaje de datos.
- Porcentaje de minutos.

Archivo:

```txt
frontend/src/app/features/usage/services/usage-api.service.spec.ts
```

### 3. UsageDashboardComponent

Valida que el dashboard muestre un mensaje amigable cuando la API falla por indisponibilidad del backend.

Mensaje esperado:

```txt
No pudimos conectar con el backend
```

Archivo:

```txt
frontend/src/app/features/usage/pages/usage-dashboard/usage-dashboard.component.spec.ts
```

## Pruebas manuales de API

Primero levantar el stack:

```bash
docker compose up --build
```

### Health check

```bash
curl http://localhost:5001/api/health
```

Respuesta esperada:

```json
{
  "status": "ok"
}
```

### Cliente principal

```bash
curl http://localhost:5001/api/customers/1001/usage
```

Resultado esperado:

- Status `200`.
- Cliente `Ana Torres`.
- Saldo `18.75`.
- Consumo de datos y minutos.

### Segundo cliente demo

```bash
curl http://localhost:5001/api/customers/1002/usage
```

Resultado esperado:

- Status `200`.
- Cliente `Carlos Mejia`.
- Datos provenientes de MySQL.

### Cliente inexistente

```bash
curl http://localhost:5001/api/customers/9999/usage
```

Resultado esperado:

- Status `404`.
- Error `customer_not_found`.

## Pruebas manuales de frontend

Levantar la aplicacion:

```bash
docker compose up --build
```

Abrir:

```txt
http://localhost:4200
```

Validar:

- El dashboard carga sin errores.
- Se muestra el nombre del cliente.
- Se muestra el saldo disponible.
- Se muestra el consumo de datos.
- Se muestra el consumo de minutos.
- Las barras de progreso tienen porcentaje correcto.
- Se muestra la fecha de ultima actualizacion.
- El boton `Actualizar` vuelve a consultar el backend.

## Prueba de error de conexion en UI

Este caso valida que la interfaz muestre un mensaje amigable cuando el backend no esta disponible.

Pasos:

1. Levantar la aplicacion:

```bash
docker compose up --build
```

2. Abrir:

```txt
http://localhost:4200
```

3. Detener los servicios con:

```bash
Ctrl + C
```

4. Volver a abrir la UI o presionar el boton `Actualizar` cuando el backend este detenido.

Resultado esperado:

```txt
No pudimos conectar con el backend. Verifica que el servicio este encendido e intenta nuevamente.
```

## Prueba de reinicio desde cero

Este caso valida que MySQL se inicialice correctamente desde `infra/mysql/init.sql`.

Ejecutar:

```bash
docker compose down -v
docker compose up --build
```

Luego probar:

```bash
curl http://localhost:5001/api/customers/1001/usage
curl http://localhost:5001/api/customers/1002/usage
```

Resultado esperado:

- Ambos clientes existen.
- Los datos se cargan nuevamente desde el seed SQL.


