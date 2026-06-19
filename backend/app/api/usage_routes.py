from flask import Blueprint, jsonify

from app.services.mock_bss_service import CustomerNotFoundError, get_customer_usage


usage_bp = Blueprint("usage", __name__, url_prefix="/api")


@usage_bp.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@usage_bp.get("/customers/<customer_id>/usage")
def customer_usage(customer_id):
    try:
        usage = get_customer_usage(customer_id)
        return jsonify(usage), 200
    except CustomerNotFoundError:
        return jsonify({
            "error": "customer_not_found",
            "message": "No encontramos informacion de consumo para este cliente."
        }), 404
    except Exception:
        return jsonify({
            "error": "internal_server_error",
            "message": "No pudimos consultar el consumo en este momento."
        }), 500