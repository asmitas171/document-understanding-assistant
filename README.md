# Document Understanding Assistant

## Project Overview
The Document Understanding Assistant is a Python-based application that extracts important information from invoice documents. It identifies invoice details, validates the extracted data, generates a summary, and highlights fields that need human review.

## Features
- Upload PDF and DOCX documents.
- Extract text from uploaded documents.
- Identify invoice number, customer name, date, total amount, and payment status.
- Validate extracted information.
- Generate a short document summary.
- Display validation errors and warnings.
- Provide field-level pattern-match indicators.
- Identify incorrect fields and flag them for human review.
- Evaluate extraction results against expected values.

## Technologies Used
- Python
- FastAPI
- PyMuPDF
- python-docx
- HTML
- CSS
- JavaScript
- Pydantic

## Project Structure
```text
Task 2/
├── app/
│   ├── main.py
│   ├── extraction.py
│   ├── baseline.py
│   ├── ai_processor.py
│   ├── validator.py
│   ├── summarizer.py
│   ├── evaluator.py
│   └── error_analysis.py
├── data/
│   ├── input/
│   └── evaluation/
│       └── expected_results.json
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── tests/
│   ├── test_extraction.py
│   ├── test_evaluation.py
│   ├── test_error_analysis.py
│   └── test_validation.py
└── README.md
```

## Setup Instructions

### 1. Create and activate a virtual environment
```powershell
python -m venv