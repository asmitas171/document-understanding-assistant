
from app.error_analysis import analyze_errors

sample_evaluation = {
    "field_results": {
        "invoice_number": {
            "expected": "INV-1001",
            "predicted": "INV-1001",
            "correct": True
        },
        "total_amount": {
            "expected": "INR 25000",
            "predicted": "INR 2500",
            "correct": False
        }
    }
}

result = analyze_errors(sample_evaluation)

print("\n===== ERROR ANALYSIS =====")
print(result)
