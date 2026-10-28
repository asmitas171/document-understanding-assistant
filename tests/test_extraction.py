
from app.extraction import extract_text
from app.ai_processor import process_document
import json

file_path = "data/input/sample_invoice.docx"

try:
    text = extract_text(file_path)
    result = process_document(text)

    print("\n===== PROTOTYPE PROCESSING RESULT =====")
    print(json.dumps(result, indent=4))

except Exception as error:
    print(f"ERROR: {error}")
