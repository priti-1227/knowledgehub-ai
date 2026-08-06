from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_processor import DocumentProcessor

router = APIRouter(tags=["Document Processing"])
processor = DocumentProcessor()

@router.post("/process-document")
async def process_document(file: UploadFile = File(...)):
    """
    Accepts a PDF, DOCX, or TXT file, extracts its text, 
    and returns text chunks.
    """
    allowed_extensions = ["pdf", "docx", "txt"]
    file_ext = file.filename.split(".")[-1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed formats: {allowed_extensions}"
        )

    try:
        # Read file bytes into memory
        file_bytes = await file.read()

        # 1. Extract raw text
        raw_text = await processor.extract_text(file_bytes, file.filename)

        # 2. Chop into chunks
        chunks = processor.create_chunks(raw_text)

        return {
            "success": True,
            "message": f"Successfully processed {file.filename}",
            "data": {
                "filename": file.filename,
                "total_characters": len(raw_text),
                "total_chunks": len(chunks),
                "sample_chunks": chunks[:3]  # Return first 3 chunks as preview
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))