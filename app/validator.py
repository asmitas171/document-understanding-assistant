
import re
from datetime import datetime


def validate_entities(data):
    """Validate extracted invoice information."""

    errors = []
    warnings = []

    # Check required fields
    required_fields = [
        "invoice_number",
        "customer",
        "date",
        "total_amount",
        "payment_status"
    ]

    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")

    # Validate invoice number
    invoice_number = data.get("invoice_number")
    if invoice_number and not re.fullmatch(
        r"[A-Za-z0-9-]+", invoice_number
    ):
        errors.append("Invalid invoice number format.")

    # Validate date
    date_value = data.get("date")
    if date_value:
        valid_date = False

        for date_format in ("%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y"):
            try:
                datetime.strptime(date_value, date_format)
                valid_date = True
                break
            except ValueError:
                pass

        if not valid_date:
            errors.append("Invalid date format or date value.")

    # Validate total amount
    amount_value = data.get("total_amount")
    if amount_value:
        amount_match = re.search(
            r"(\d+(?:,\d{3})*(?:\.\d{1,2})?)$",
            amount_value.replace(" ", "")
        )

        if not amount_match:
            errors.append("Invalid total amount.")
        elif float(amount_match.group(1).replace(",", "")) < 0:
            errors.append("Total amount cannot be negative.")

    # Validate payment status
    payment_status = data.get("payment_status")
    if payment_status and payment_status.lower() not in [
        "paid", "pending", "overdue", "unpaid"
    ]:
        warnings.append("Unrecognized payment status. Please review.")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
