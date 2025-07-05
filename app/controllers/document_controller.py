import os
import base64
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.services.ocr_service import process_document
from app.services.cloud_storage import upload_to_local_storage, upload_to_gcp
from app.models.db import save_document_to_db

document_controller = APIRouter()

@document_controller.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        file_data = base64.b64encode(file_bytes).decode("utf-8")
        file_name = file.filename

        # Procesa el documento y extrae campos
        document_type, document_text, fields = process_document(file_data, file_name)

        # Guarda el archivo
        if os.getenv('GCP_PROJECT') is None:
            file_path = upload_to_local_storage(file_data, file_name)
        else:
            file_path = upload_to_gcp(file_data, file_name)

        document_info = {
            "doc_type": document_type,
            "is_legible": True,
            "raw_text": document_text,
            "first_name": fields.get("first_name", ""),
            "last_name": fields.get("last_name", ""),
            "document_number": fields.get("document_number", ""),
            "birth_date": fields.get("birth_date", ""),
            "birth_place": fields.get("birth_place", ""),
            "height": fields.get("height", ""),
            "blood_type": fields.get("blood_type", ""),
            "gender": fields.get("gender", ""),
            "issue_date": fields.get("issue_date", ""),
            "issue_place": fields.get("issue_place", ""),
            "file_path": file_path
        }

        save_document_to_db(document_info)

        return {
            "status": "success",
            "document_type": document_type,
            "document_text": document_text,
            "fields": fields,
            "file_path": file_path
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
