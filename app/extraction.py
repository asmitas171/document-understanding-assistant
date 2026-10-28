import pymupdf as fitz
from docx import Document
from pathlib import Path


def extract_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""

    try:
        document = fitz.open(file_path)

        for page in document:
            text += page.get_text()

        document.close()

        return text.strip()

    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")


def extract_from_docx(file_path):
    """Extract text from a DOCX file."""
    text = ""

    try:
        document = Document(file_path)

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text.strip()

    except Exception as e:
        raise Exception(f"Error reading DOCX: {e}")


def extract_text(file_path):
    """Detect file type and extract text."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("The specified file does not exist.")

    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_from_pdf(file_path)

    elif extension == ".docx":
        return extract_from_docx(file_path)

    else:
        raise ValueError(
            "Unsupported file type. Please upload a PDF or DOCX file."
        )