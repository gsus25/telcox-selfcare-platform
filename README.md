# TelcoX Selfcare Platform

Plataforma web de autogestion para clientes de telecomunicaciones. Permite visualizar saldo disponible, consumo de datos moviles y minutos disponibles mediante una interfaz conectada a un backend REST que simula la integracion con sistemas BSS/CRM.

## Objetivo del reto

El proyecto implementa un flujo end-to-end para el modulo de visualizacion de consumo:

Angular UI -> Flask REST API -> MySQL -> respuesta al usuario

La aplicacion esta enfocada en demostrar:
- Integracion frontend-backend.
- Consulta de consumo de cliente.
- Manejo de estados de carga, exito y error en la interfaz.
- Backend REST con manejo de excepciones.
- Persistencia demo en MySQL.
- Contenerizacion con Docker Compose.
- Pruebas automatizadas backend y frontend.

## Stack Tecnologico

- Frontend: Angular 19 (Standalone Components), TypeScript, CSS, Bootstrap.
- Backend: Python 3.12, Flask, Flask-CORS.
- Base de datos: MySQL.
- Testing: pytest (Backend) / Angular TestBed, Jasmine, Karma, ChromeHeadless (Frontend).
- DevOps: Docker, Docker Compose.

## Requisitos Previos

- Docker Desktop instalado y en ejecucion.
- Docker Compose disponible.

## Variables de Entorno

El archivo .env.example documenta las variables usadas por la solucion:

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

## Ejecutar la Aplicacion

Desde la raiz del proyecto, inicializa los contenedores:

docker compose up --build

Servicios disponibles:
- Frontend: http://localhost:4200
- Backend:  http://localhost:5001/api/health
- MySQL:    localhost:3307 (No expone interfaz web, accesible via cliente SQL).

Para detener los servicios:
docker compose down

Para reiniciar desde cero (incluyendo la eliminacion de volumenes de base de datos):
docker compose down -v
docker compose up --build

## Documentacion del Proyecto

Toda la documentacion tecnica se encuentra en la carpeta /docs:
- Arquitectura y Decisiones Tecnicas: ./docs/architecture.md
- Documentacion de la API: ./docs/api.md
- Estrategia de Pruebas: ./docs/testing.md
