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

Flujo principal de la solucion:

```txt
Usuario -> Angular Dashboard -> Flask API -> Servicio BSS simulado -> MySQL
```

El frontend consume una API REST del backend. El backend delega la consulta de consumo a un servicio que simula la integracion con BSS/CRM y obtiene los datos desde MySQL.

Para un desglose completo de la estructura de carpetas, patrones de diseno, responsabilidades y flujo de datos, revisa la [Documentacion de Arquitectura](./docs/architecture.md).

## Decisiones tecnicas

### Cliente autenticado simulado

El reto se centra en el modulo de visualizacion de consumo, no en autenticacion. Por eso el frontend consulta el cliente demo `1001`.

En una implementacion productiva, el `customerId` vendria desde la sesion autenticada, token JWT o integracion con CRM.

### Simulacion BSS/CRM

El backend contiene un servicio llamado `mock_bss_service.py`. Este servicio representa la integracion con un sistema BSS/CRM. Para efectos del reto, los datos se almacenan en MySQL mediante un seed inicial.

Esto permite demostrar una integracion real de backend con base de datos sin construir un BSS completo.

### Puerto backend

El backend corre internamente en el puerto `5000`, pero se expone localmente en `5001`

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
Backend:  http://localhost:5001/api/health
MySQL:    localhost:3307
```

Nota: MySQL no expone una interfaz web. El puerto `3307` queda disponible para conectarse desde un cliente MySQL local usando las credenciales documentadas en `.env.example`.

Para detener los servicios:

```bash
docker compose down
```

Para reiniciar desde cero, incluyendo la base de datos:

```bash
docker compose down -v
docker compose up --build
```

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

El dashboard consulta por defecto el cliente `1001`, simulando un usuario autenticado.

## API REST

El backend expone endpoints para consultar el estado de salud del sistema y el consumo del cliente.

Para ver los contratos de los endpoints, ejemplos de peticiones/respuestas JSON y codigos de error, consulta la [Documentacion de la API](./docs/api.md).

## Ejecutar pruebas

Backend:

```bash
docker compose run --rm backend pytest
```

Frontend:

```bash
cd frontend
npm test -- --watch=false --browsers=ChromeHeadless
```

Para detalles sobre la estrategia de testing, herramientas utilizadas y cobertura, visita la [Documentacion de Pruebas](./docs/testing.md).