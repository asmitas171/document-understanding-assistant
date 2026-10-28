
def analyze_errors(evaluation):
    """Identify incorrect fields from evaluation results."""
    field_results = evaluation.get("field_results", {})
    incorrect_fields = []

    for field, result in field_results.items():
        if not result.get("correct", False):
            incorrect_fields.append({
                "field": field,
                "expected": result.get("expected"),
                "predicted": result.get("predicted"),
                "action": "Human review required"
            })

    return {
        "total_fields": len(field_results),
        "incorrect_fields": incorrect_fields,
        "review_required": len(incorrect_fields) > 0
    }
