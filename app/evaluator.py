
def evaluate_entities(expected, predicted):
    """Compare extracted fields with the expected results."""

    total_fields = len(expected)
    correct_fields = 0
    field_results = {}

    for field, expected_value in expected.items():
        predicted_value = predicted.get(field)

        is_correct = (
            predicted_value is not None
            and str(predicted_value).strip().casefold()
            == str(expected_value).strip().casefold()
        )

        if is_correct:
            correct_fields += 1

        field_results[field] = {
            "expected": expected_value,
            "predicted": predicted_value,
            "correct": is_correct
        }

    accuracy = (
        correct_fields / total_fields * 100
        if total_fields else 0
    )

    return {
        "correct_fields": correct_fields,
        "total_fields": total_fields,
        "accuracy_percent": round(accuracy, 2),
        "field_results": field_results
    }
