
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

from app.extraction import extract_text
from app.baseline import extract_entities
from app.ai_processor import process_document
from app.validator import validate_entities
from app.summarizer import summarize_document

app = FastAPI(title="Document Understanding Assistant")

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "input"
STATIC_DIR = BASE_DIR / "static"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def home():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    allowed_extensions = {".pdf", ".docx"}
    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    saved_path = UPLOAD_DIR / f"uploaded_document{extension}"

    try:
        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 1: Extract document text
        text = extract_text(str(saved_path))

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text found. Scanned PDFs may need OCR."
            )

        # Step 2: Extract invoice entities
        entities = extract_entities(text)

        # Step 3: Validate extracted entities
        validation = validate_entities(entities)

        # Step 4: Generate document summary
        summary = summarize_document(entities)

        # Step 5: Run the prototype processor
        prototype_result = process_document(text)
        review_required = prototype_result["review_required"]

        # Step 6: Decide whether human review is needed
        human_review = {
            "required": (
                bool(review_required)
                or not validation.get("is_valid", False)
            ),
            "fields": review_required,
            "validation_errors": validation.get("errors", []),
            "validation_warnings": validation.get("warnings", [])
        }

        # Step 7: Return the complete result
        return {
            "filename": file.filename,
            "extracted_text": text,
            "entities": entities,
            "validation": validation,
            "summary": summary,
            "prototype_result": prototype_result,
            "human_review": human_review
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {error}"
        )

    finally:
        await file.close()
