# Testing Documentation

La estrategia de pruebas de TelcoX Selfcare Platform cubre la validacion unitaria y de integracion en ambas capas de la aplicacion (Frontend y Backend).

## 1. Pruebas Backend (pytest)

El backend utiliza pytest para validar la logica de la API y el manejo de excepciones. Las variables de entorno son aisladas y el servicio BSS es emulado usando monkeypatch para evitar dependencia directa de MySQL durante los tests unitarios, garantizando velocidad y estabilidad.

Ejecucion:
Desde la raiz del proyecto, ejecuta el contenedor de pruebas:

```bash
docker compose run --rm backend pytest
```

Resultado esperado: 4 passed

Casos Cubiertos:
- test_health_check: Valida el status 200 OK.
- test_successful_usage: Verifica que el contrato JSON retorne la estructura correcta y calcule los porcentajes adecuados.
- test_customer_not_found: Valida la respuesta 404 estructurada.
- test_bss_unavailable: Simula una caida del servicio MySQL y valida el codigo 503.

## 2. Pruebas Frontend (Angular TestBed)

Las pruebas de frontend validan la renderizacion del DOM, la interaccion de los servicios y el manejo de estados visuales.

Ejecucion:

```bash
cd frontend
npm test -- --watch=false --browsers=ChromeHeadless
```

Resultado esperado: TOTAL: 3 SUCCESS

Casos Cubiertos:
- AppComponent: Valida la carga del App Shell.
- UsageApiService: Intercepta peticiones HTTP para asegurar que el servicio solicita el endpoint correcto (GET /api/customers/1001/usage) y mapea bien el payload.
- UsageDashboardComponent: Renderiza el componente forzando un error en el servicio, verificando que el DOM muestre el mensaje amigable: "No pudimos conectar con el backend".

## 3. Pruebas de Integracion Manual (End-to-End Visual)

Para validar la integracion real entre contenedores (UI -> API -> DB):
1. Levanta el stack: docker compose up --build
2. Ingresa a http://localhost:4200
3. Valida que los datos de "Ana Torres" (Seed de MySQL) se muestren correctamente.
4. Prueba de Resiliencia: Deten el servicio mysql temporalmente (docker compose stop mysql) y da clic en "Actualizar" en el dashboard. Deberas observar el manejo de error en la UI.

*(Para los comandos precisos de validacion de endpoints via consola, consulta la Documentacion de la API (api.md)).*

