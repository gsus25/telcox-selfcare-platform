from datetime import datetime, timezone

from app.main import create_app
from app.services.mock_bss_service import BssUnavailableError, CustomerNotFoundError


def test_health_check_returns_ok():
    app = create_app()

    with app.test_client() as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_customer_usage_returns_expected_payload(monkeypatch):
    def mock_get_customer_usage(customer_id):
        return {
            "customerId": customer_id,
            "customerName": "Ana Torres",
            "balance": 18.75,
            "dataUsage": {
                "used": 7.2,
                "total": 20,
                "unit": "GB",
                "percentage": 36,
            },
            "minutesUsage": {
                "used": 320,
                "total": 1000,
                "unit": "minutes",
                "percentage": 32,
            },
            "lastUpdated": datetime.now(timezone.utc).isoformat(),
        }

    monkeypatch.setattr(
        "app.api.usage_routes.get_customer_usage",
        mock_get_customer_usage,
    )

    app = create_app()

    with app.test_client() as client:
        response = client.get("/api/customers/1001/usage")

    body = response.get_json()

    assert response.status_code == 200
    assert body["customerId"] == "1001"
    assert body["customerName"] == "Ana Torres"
    assert body["balance"] == 18.75
    assert body["dataUsage"]["percentage"] == 36
    assert body["minutesUsage"]["percentage"] == 32
    assert "lastUpdated" in body


def test_customer_usage_returns_404_when_customer_does_not_exist(monkeypatch):
    def mock_get_customer_usage(customer_id):
        raise CustomerNotFoundError()

    monkeypatch.setattr(
        "app.api.usage_routes.get_customer_usage",
        mock_get_customer_usage,
    )

    app = create_app()

    with app.test_client() as client:
        response = client.get("/api/customers/9999/usage")

    body = response.get_json()

    assert response.status_code == 404
    assert body["error"] == "customer_not_found"
    assert body["message"] == "No encontramos informacion de consumo para este cliente."


def test_customer_usage_returns_503_when_bss_is_unavailable(monkeypatch):
    def mock_get_customer_usage(customer_id):
        raise BssUnavailableError()

    monkeypatch.setattr(
        "app.api.usage_routes.get_customer_usage",
        mock_get_customer_usage,
    )

    app = create_app()

    with app.test_client() as client:
        response = client.get("/api/customers/1001/usage")

    body = response.get_json()

    assert response.status_code == 503
    assert body["error"] == "bss_unavailable"
    assert body["message"] == "El sistema BSS no esta disponible temporalmente."