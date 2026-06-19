from datetime import datetime, timezone


class CustomerNotFoundError(Exception):
    pass


MOCK_USAGE = {
    "1001": {
        "customerId": "1001",
        "customerName": "Ana Torres",
        "balance": 18.75,
        "dataUsage": {
            "used": 7.2,
            "total": 20,
            "unit": "GB"
        },
        "minutesUsage": {
            "used": 320,
            "total": 1000,
            "unit": "minutes"
        }
    }
}


def calculate_percentage(used, total):
    if total <= 0:
        return 0

    return round((used / total) * 100)


def get_customer_usage(customer_id):
    usage = MOCK_USAGE.get(customer_id)

    if usage is None:
        raise CustomerNotFoundError()

    data_usage = usage["dataUsage"]
    minutes_usage = usage["minutesUsage"]

    return {
        **usage,
        "dataUsage": {
            **data_usage,
            "percentage": calculate_percentage(data_usage["used"], data_usage["total"])
        },
        "minutesUsage": {
            **minutes_usage,
            "percentage": calculate_percentage(minutes_usage["used"], minutes_usage["total"])
        },
        "lastUpdated": datetime.now(timezone.utc).isoformat()
    }
