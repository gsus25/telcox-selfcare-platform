import os
from datetime import timezone

import pymysql


class CustomerNotFoundError(Exception):
    pass


class BssUnavailableError(Exception):
    pass


def get_database_connection():
    try:
        return pymysql.connect(
            host=os.getenv("DATABASE_HOST", "mysql"),
            port=int(os.getenv("DATABASE_PORT", "3306")),
            user=os.getenv("DATABASE_USER", "telcox_user"),
            password=os.getenv("DATABASE_PASSWORD", "telcox_password"),
            database=os.getenv("DATABASE_NAME", "telcox_db"),
            cursorclass=pymysql.cursors.DictCursor,
        )
    except pymysql.MySQLError as error:
        raise BssUnavailableError() from error


def calculate_percentage(used, total):
    if total <= 0:
        return 0

    return round((float(used) / float(total)) * 100)


def get_customer_usage(customer_id):
    query = """
        SELECT
            customer_id,
            customer_name,
            balance,
            data_used,
            data_total,
            minutes_used,
            minutes_total,
            updated_at
        FROM customer_usage
        WHERE customer_id = %s
    """

    try:
        connection = get_database_connection()

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (customer_id,))
                row = cursor.fetchone()
    except pymysql.MySQLError as error:
        raise BssUnavailableError() from error

    if row is None:
        raise CustomerNotFoundError()

    data_used = float(row["data_used"])
    data_total = float(row["data_total"])
    minutes_used = int(row["minutes_used"])
    minutes_total = int(row["minutes_total"])

    updated_at = row["updated_at"]
    if updated_at.tzinfo is None:
        updated_at = updated_at.replace(tzinfo=timezone.utc)

    return {
        "customerId": row["customer_id"],
        "customerName": row["customer_name"],
        "balance": float(row["balance"]),
        "dataUsage": {
            "used": data_used,
            "total": data_total,
            "unit": "GB",
            "percentage": calculate_percentage(data_used, data_total),
        },
        "minutesUsage": {
            "used": minutes_used,
            "total": minutes_total,
            "unit": "minutes",
            "percentage": calculate_percentage(minutes_used, minutes_total),
        },
        "lastUpdated": updated_at.isoformat(),
    }