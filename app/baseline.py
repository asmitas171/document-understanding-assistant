
import re


def extract_entities(text):
    """Extract invoice details using simple rules."""

    patterns = {
        "invoice_number": r"Invoice Number:\s*(.+)",
        "customer": r"Customer:\s*(.+)",
        "date": r"Date:\s*(.+)",
        "total_amount": r"Total Amount:\s*(.+)",
        "payment_status": r"Payment Status:\s*(.+)"
    }

    result = {}

    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            result[field] = match.group(1).strip()
        else:
            result[field] = None

    return result
