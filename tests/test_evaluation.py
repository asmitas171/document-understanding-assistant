
import json
from pathlib import Path

from app.extraction import extract_text
from app.error_analysis import analyze_errors
from app.baseline import extract_entities
from app.ai_processor import process_document
from app.evaluator import evaluate_entities

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DIR = BASE_DIR / "data" / "input"
EXPECTED_FILE = BASE_DIR / "data" / "evaluation" / "expected_results.json"


def main():
    with EXPECTED_FILE.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    baseline_total_correct = 0
    prototype_total_correct = 0
    total_fields = 0

    for filename, expected in dataset.items():
        input_file = INPUT_DIR / filename

        print(f"\n{'=' * 50}")
        print(f"Evaluating: {filename}")
        print("=" * 50)

        if not input_file.exists():
            print(f"FILE NOT FOUND: {input_file}")
            continue

        text = extract_text(str(input_file))

        baseline_result = extract_entities(text)
        prototype_output = process_document(text)
        prototype_result = prototype_output["entities"]

        baseline_evaluation = evaluate_entities(
            expected, baseline_result
        )

        prototype_evaluation = evaluate_entities(
            expected, prototype_result
        )

        print("\n--- BASELINE EVALUATION ---")
        print(json.dumps(baseline_evaluation, indent=4))

        print("\n--- PROTOTYPE EVALUATION ---")
        print(json.dumps(prototype_evaluation, indent=4))

        print("\n--- PROTOTYPE REVIEW FLAGS ---")
        print(json.dumps(prototype_output["review_required"], indent=4))

        print("\n--- BASELINE ERROR ANALYSIS ---")
        print(json.dumps(analyze_errors(baseline_evaluation), indent=4))

        print("\n--- PROTOTYPE ERROR ANALYSIS ---")
        print(json.dumps(analyze_errors(prototype_evaluation), indent=4))

        baseline_total_correct += baseline_evaluation["correct_fields"]
        prototype_total_correct += prototype_evaluation["correct_fields"]
        total_fields += baseline_evaluation["total_fields"]

    print("\n" + "=" * 50)
    print("FINAL COMPARISON")
    print("=" * 50)

    if total_fields:
        baseline_accuracy = baseline_total_correct / total_fields * 100
        prototype_accuracy = prototype_total_correct / total_fields * 100

        print(f"Total fields evaluated: {total_fields}")
        print(
            f"Baseline: {baseline_total_correct}/{total_fields} "
            f"({baseline_accuracy:.2f}%)"
        )
        print(
            f"Prototype: {prototype_total_correct}/{total_fields} "
            f"({prototype_accuracy:.2f}%)"
        )
    else:
        print("No fields were evaluated. Check your files and dataset.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}")
