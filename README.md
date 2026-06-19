# TelcoX Selfcare Platform

Plataforma web de auto-gestion para clientes de telecomunicaciones. Permite visualizar saldo disponible, consumo de datos moviles y minutos disponibles mediante una interfaz conectada a un backend REST que simula la integracion con sistemas BSS/CRM.

## Objetivo del reto

El proyecto implementa un flujo end to end para el modulo de visualizacion de consumo:

```txt
Angular UI -> Flask REST API -> MySQL -> respuesta al usuario
```

La aplicacion esta enfocada en demostrar:

- Integracion frontend-backend.
- Consulta de consumo de cliente.
- Manejo de estados de carga, exito y error en la interfaz.
- Backend REST con manejo de excepciones.
- Persistencia demo en MySQL.
- Contenerizacion con Docker Compose.
- Pruebas automatizadas backend y frontend.

## Stack tecnologico

- Frontend: Angular, TypeScript, CSS, Bootstrap.
- Backend: Python, Flask, Flask-CORS.
- Base de datos: MySQL.
- Testing backend: pytest.
- Testing frontend: Angular TestBed, Jasmine, Karma, ChromeHeadless.
- DevOps: Docker, Docker Compose.

## Arquitectura

```txt
telcox-selfcare-platform/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── usage_routes.py
│   │   ├── services/
│   │   │   └── mock_bss_service.py
│   │   └── main.py
│   ├── tests/
│   │   └── test_usage.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   └── app/
│   │       └── features/
│   │           └── usage/
│   ├── Dockerfile
│   └── package.json
│
├── infra/
│   └── mysql/
│       └── init.sql
│
├── docs/
├── docker-compose.yml
└── README.md
```

## Decisiones tecnicas

### Cliente autenticado simulado

El reto se centra en el modulo de visualizacion de consumo, no en autenticacion. Por eso el frontend consulta el cliente demo `1001`.

En una implementacion productiva, el `customerId` vendria desde la sesion autenticada, token JWT o integracion con CRM.

### Simulacion BSS/CRM

El backend contiene un servicio llamado `mock_bss_service.py`. Este servicio representa la integracion con un sistema BSS/CRM. Para efectos del reto, los datos se almacenan en MySQL mediante un seed inicial.

Esto permite demostrar una integracion real de backend con base de datos sin construir un BSS completo.

### Puerto backend

El backend corre internamente en el puerto `5000`, pero se expone localmente en `5001` para evitar conflictos comunes con servicios locales en macOS.

## Requisitos previos

- Docker Desktop instalado y en ejecucion.
- Docker Compose disponible.

Opcional para desarrollo local sin Docker:

- Node.js compatible con Angular 19.
- Python 3.12.

## Variables de entorno

El archivo `.env.example` documenta las variables usadas por la solucion:

```env
MYSQL_DATABASE=telcox_db
MYSQL_USER=telcox_user
MYSQL_PASSWORD=telcox_password
MYSQL_ROOT_PASSWORD=root_password

BACKEND_PORT=5001
FRONTEND_PORT=4200

DATABASE_HOST=mysql
DATABASE_PORT=3306
DATABASE_NAME=telcox_db
DATABASE_USER=telcox_user
DATABASE_PASSWORD=telcox_password
```

## Ejecutar la aplicacion

Desde la raiz del proyecto:

```bash
docker compose up --build
```

Servicios disponibles:

```txt
Frontend: http://localhost:4200
Backend:  http://localhost:5001
MySQL:    localhost:3307
```

Para detener los servicios:

```bash
docker compose down
```

Para reiniciar desde cero, incluyendo la base de datos:

```bash
docker compose down -v
docker compose up --build
```

## Endpoints principales

Health check:

```http
GET /api/health
```

URL local:

```txt
http://localhost:5001/api/health
```

Consulta de consumo:

```http
GET /api/customers/{customerId}/usage
```

Cliente demo principal:

```txt
http://localhost:5001/api/customers/1001/usage
```

Segundo cliente demo:

```txt
http://localhost:5001/api/customers/1002/usage
```

Cliente inexistente:

```txt
http://localhost:5001/api/customers/9999/usage
```

## Ejemplo de respuesta exitosa

```json
{
  "customerId": "1001",
  "customerName": "Ana Torres",
  "balance": 18.75,
  "dataUsage": {
    "used": 7.2,
    "total": 20.0,
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
```

## Manejo de errores

La API maneja los siguientes casos:

```txt
404 customer_not_found
Cliente no encontrado.

503 bss_unavailable
El sistema BSS/MySQL no esta disponible temporalmente.

500 internal_server_error
Error inesperado del backend.
```

La interfaz muestra mensajes amigables cuando:

- El backend no esta disponible.
- No existe informacion para el cliente.
- Ocurre un error inesperado al consultar el consumo.

## Ejecutar pruebas

### Backend

Con Docker:

```bash
docker compose run --rm backend pytest
```

Resultado esperado:

```txt
4 passed
```

Las pruebas backend cubren:

- Health check.
- Consulta exitosa de consumo.
- Cliente no encontrado.
- BSS no disponible.

### Frontend

Desde la carpeta `frontend`:

```bash
cd frontend
npm test -- --watch=false --browsers=ChromeHeadless
```

Resultado esperado:

```txt
TOTAL: 3 SUCCESS
```

Las pruebas frontend cubren:

- Creacion del shell principal de Angular.
- Servicio `UsageApiService`, validando que llama correctamente al endpoint de consumo.
- Componente `UsageDashboardComponent`, validando que muestra un mensaje amigable cuando el backend no esta disponible.

## Datos demo

Los datos iniciales se cargan desde:

```txt
infra/mysql/init.sql
```

Clientes disponibles:

```txt
1001 - Ana Torres
1002 - Carlos Mejia
```

## Flujo de uso

1. El usuario abre el dashboard en `http://localhost:4200`.
2. Angular solicita el consumo del cliente demo `1001`.
3. Flask recibe la solicitud en `/api/customers/1001/usage`.
4. El servicio simula la consulta al BSS usando MySQL.
5. La API responde saldo, datos, minutos y fecha de actualizacion.
6. La interfaz muestra la informacion en tarjetas visuales con barras de progreso.