
import re
from app.baseline import extract_entities


def process_document(text):
    """Prototype processor with field-level confidence indicators.

    This is a rule-based prototype, not a real AI model.
    """

    entities = extract_entities(text)
    confidence = {}
    review_required = []

    patterns = {
        "invoice_number": r"Invoice Number:\s*\S+",
        "customer": r"Customer:\s*.+",
        "date": r"Date:\s*\d{1,2}[/-]\d{1,2}[/-]\d{4}",
        "total_amount": r"Total Amount:\s*(?:INR|Rs\.?|₹)?\s*[\d,]+(?:\.\d{1,2})?",
        "payment_status": r"Payment Status:\s*(?:Paid|Pending|Overdue|Unpaid)"
    }

    for field, pattern in patterns.items():
        value = entities.get(field)

        if value and re.search(pattern, text, re.IGNORECASE):
            confidence[field] = 0.95
        else:
            confidence[field] = 0.0
            review_required.append(field)

    return {
        "entities": entities,
        "confidence": confidence,
        "review_required": review_required
    }
