from app.main import create_app


def test_health_check_returns_ok():
    app = create_app()

    with app.test_client() as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_customer_usage_returns_expected_payload():
    app = create_app()

    with app.test_client() as client:
        response = client.get("/api/customers/1001/usage")

    body = response.get_json()

    assert response.status_code == 200
    assert body["customerId"] == "1001"
    assert body["customerName"] == "Ana Torres"
    assert body["balance"] == 18.75

    assert body["dataUsage"]["used"] == 7.2
    assert body["dataUsage"]["total"] == 20
    assert body["dataUsage"]["unit"] == "GB"
    assert body["dataUsage"]["percentage"] == 36

    assert body["minutesUsage"]["used"] == 320
    assert body["minutesUsage"]["total"] == 1000
    assert body["minutesUsage"]["unit"] == "minutes"
    assert body["minutesUsage"]["percentage"] == 32

    assert "lastUpdated" in body


def test_customer_usage_returns_404_when_customer_does_not_exist():
    app = create_app()

    with app.test_client() as client:
        response = client.get("/api/customers/9999/usage")

    body = response.get_json()

    assert response.status_code == 404
    assert body["error"] == "customer_not_found"
    assert body["message"] == "No encontramos informacion de consumo para este cliente."