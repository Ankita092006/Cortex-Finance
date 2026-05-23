from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.services.pdf_parser import extract_transactions

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transactions = extract_transactions(file_path)

    return {
        "success": True,
        "filename": file.filename,
        "transaction_count": len(transactions),
        "transactions": transactions[:10]
    }