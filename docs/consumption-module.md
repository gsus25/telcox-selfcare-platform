# Consumption Module Documentation

Documentacion del modulo de visualizacion de consumo de TelcoX Selfcare Platform.

## Proposito

El modulo de consumo permite que un cliente de telecomunicaciones visualice de forma clara su informacion principal de uso:

- Saldo disponible.
- Consumo de datos moviles.
- Consumo de minutos.
- Estado del servicio.
- Fecha/hora de ultima consulta.

Este modulo busca reducir consultas de soporte al entregar al usuario informacion de autogestion en una pantalla simple, visual y actualizable.

## Alcance implementado

El modulo implementa una rebanada end to end:

```txt
Dashboard Angular -> Servicio HTTP Angular -> Flask API -> Servicio BSS simulado -> MySQL
```

El usuario abre el dashboard, el frontend consulta el consumo del cliente demo `1001`, el backend obtiene la informacion desde MySQL y la interfaz presenta los datos en tarjetas visuales.

## Experiencia de usuario

El dashboard muestra la informacion priorizada como en una plataforma telco de autogestion:

1. Identificacion del cliente.
2. Saldo disponible.
3. Consumo de datos moviles con porcentaje y barra de progreso.
4. Consumo de minutos con porcentaje y barra de progreso.
5. Estado del servicio.
6. Ultima consulta realizada desde la interfaz.
7. Boton para actualizar la informacion.


## Flujo funcional

1. El usuario entra a:

```txt
http://localhost:4200
```

2. Angular carga `UsageDashboardComponent`.
3. El componente ejecuta `loadUsage()`.
4. `UsageApiService` llama al backend:

```http
GET http://localhost:5001/api/customers/1001/usage
```

5. Flask recibe la solicitud en `usage_routes.py`.
6. La ruta delega la consulta a `mock_bss_service.py`.
7. El servicio consulta la tabla `customer_usage` en MySQL.
8. El backend responde un JSON con saldo, datos, minutos y fecha de actualizacion.
9. Angular renderiza la informacion en el dashboard.

## Archivos principales

### Frontend

```txt
frontend/src/app/features/usage/models/usage.model.ts
```

Define los contratos TypeScript usados por el dashboard:

- `CustomerUsage`
- `UsageBucket`

```txt
frontend/src/app/features/usage/services/usage-api.service.ts
```

Servicio responsable de llamar a la API REST del backend.

```txt
frontend/src/app/features/usage/pages/usage-dashboard/usage-dashboard.component.ts
```

Componente principal del modulo. Maneja:

- Carga inicial.
- Refresco manual.
- Estado de loading.
- Estado de error.
- Datos exitosos.
- Calculo visual de remanentes.

```txt
frontend/src/app/features/usage/pages/usage-dashboard/usage-dashboard.component.html
```

Template visual del dashboard.

```txt
frontend/src/app/features/usage/pages/usage-dashboard/usage-dashboard.component.css
```

Estilos del dashboard, incluyendo layout, tarjetas, barras de progreso y responsive design.

### Backend

```txt
backend/app/api/usage_routes.py
```

Define los endpoints REST del modulo:

- `GET /api/health`
- `GET /api/customers/<customer_id>/usage`

```txt
backend/app/services/mock_bss_service.py
```

Simula la integracion con BSS/CRM. Consulta MySQL y transforma la informacion al contrato esperado por la API.

```txt
infra/mysql/init.sql
```

Crea la tabla `customer_usage` e inserta datos demo.

## Modelo de datos

Tabla principal:

```txt
customer_usage
```

Campos:

| Campo | Descripcion |
|---|---|
| `customer_id` | Identificador del cliente. |
| `customer_name` | Nombre del cliente. |
| `balance` | Saldo disponible. |
| `data_used` | Datos consumidos. |
| `data_total` | Total del paquete de datos. |
| `minutes_used` | Minutos consumidos. |
| `minutes_total` | Total de minutos disponibles. |
| `updated_at` | Fecha de ultima actualizacion del registro. |

## Contrato principal

El dashboard consume una respuesta con esta forma:

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

## Estados de UI

### Loading

Mientras la API responde, el dashboard muestra un estado de carga:

```txt
Consultando tu consumo en tiempo real...
```

### Success

Cuando la consulta es exitosa, se muestran las tarjetas de consumo.

### Error

Cuando la API falla, se muestra un mensaje amigable y un boton de reintento.

Casos considerados:

| Caso | Comportamiento en UI |
|---|---|
| Backend no disponible | Mensaje indicando que no se pudo conectar con el backend. |
| Cliente no encontrado | Mensaje indicando que no existe informacion para el cliente. |
| Error inesperado | Mensaje generico de fallo al consultar consumo. |

## Refresco de datos

El boton `Actualizar` ejecuta nuevamente la consulta contra el backend.

La UI puede mostrar la fecha/hora de ultima consulta para indicar al usuario cuando se refresco la informacion en pantalla.

Nota: el campo `lastUpdated` de la API representa la ultima actualizacion del dato en MySQL/BSS simulado. No necesariamente cambia en cada consulta si el registro no fue modificado.

## Datos demo

Clientes cargados por seed:

```txt
1001 - Ana Torres
1002 - Carlos Mejia
```

El frontend usa `1001` como cliente autenticado simulado.

