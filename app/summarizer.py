
def summarize_document(data):
    """Generate a simple summary of an invoice."""

    invoice_number = data.get("invoice_number") or "Not provided"
    customer = data.get("customer") or "Not provided"
    date = data.get("date") or "Not provided"
    amount = data.get("total_amount") or "Not provided"
    status = data.get("payment_status") or "Not provided"

    summary = (
        f"Invoice {invoice_number} is issued to {customer} "
        f"on {date}. The total amount is {amount}, "
        f"and the payment status is {status}."
    )

    return summary
