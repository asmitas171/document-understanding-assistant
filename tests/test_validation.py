
from pathlib import Path
from app.extraction import extract_text
from app.baseline import extract_entities
from app.validator import validate_entities

BASE_DIR = Path(__file__).resolve().parent.parent

files = [
    "sample_invoice.docx",
    "sample_invoice_2.docx",
    "sample_invoice_3.docx",
]

for filename in files:
    file_path = BASE_DIR / "data" / "input" / filename

    print(f"\n===== VALIDATION: {filename} =====")

    try:
        text = extract_text(str(file_path))
        entities = extract_entities(text)
        result = validate_entities(entities)
        print(result)
    except Exception as error:
        print(f"ERROR: {error}")
