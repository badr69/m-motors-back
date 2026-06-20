import os
import uuid
from app.core.security.extensions import ALLOWED_DOCUMENT_EXTENSIONS
from app.modules.documents.model import Document  # ✅ IMPORTANT

UPLOAD_FOLDER = "uploads/documents"


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_DOCUMENT_EXTENSIONS
    )


class DocumentService:

    # =====================
    # CREATE DOCUMENT
    # =====================
    @staticmethod
    def create_document(db, data, file):

        # =====================
        # VALIDATE FILE
        # =====================
        if not file or file.filename == "":
            return {"data": None, "error": "No file provided"}

        if not allowed_file(file.filename):
            return {"data": None, "error": "File type not allowed"}

        # =====================
        # VALIDATE DOSSIER ID
        # =====================
        dossier_id = data.get("dossier_id")

        if not dossier_id:
            return {"data": None, "error": "dossier_id required"}

        try:
            dossier_id = int(dossier_id)
        except ValueError:
            return {"data": None, "error": "invalid dossier_id"}

        # =====================
        # VALIDATE USER ID
        # =====================
        user_id = data.get("user_id")

        if not user_id:
            return {"data": None, "error": "user_id required"}

        try:
            user_id = int(user_id)
        except ValueError:
            return {"data": None, "error": "invalid user_id"}

        # =====================
        # TYPE DOCUMENT (SAFE DEFAULT)
        # =====================
        type_document = data.get("type_document") or "general"

        # =====================
        # CREATE UPLOAD FOLDER
        # =====================
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # =====================
        # GENERATE FILE NAME
        # =====================
        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        file.save(filepath)

        # =====================
        # CREATE ORM OBJECT
        # =====================
        document = Document(
            dossier_id=dossier_id,
            user_id=user_id,
            type_document=type_document,
            filename=filename,
            filepath=filepath,
            mime_type=file.mimetype
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        # =====================
        # RESPONSE
        # =====================
        return {
            "data": {
                "id": document.id,
                "dossier_id": document.dossier_id,
                "user_id": document.user_id,
                "type_document": document.type_document,
                "filename": document.filename,
                "filepath": document.filepath,
                "mime_type": document.mime_type
            },
            "error": None
        }

    # =====================
    # GET DOCUMENT BY ID
    # =====================
    @staticmethod
    def get_document_by_id(db, doc_id):

        document = db.query(Document).filter(Document.id == doc_id).first()

        if not document:
            return {"data": None, "error": "Document not found"}

        return {
            "data": {
                "id": document.id,
                "dossier_id": document.dossier_id,
                "user_id": document.user_id,
                "type_document": document.type_document,
                "filename": document.filename,
                "filepath": document.filepath,
                "mime_type": document.mime_type
            },
            "error": None
        }

    # =====================
    # GET all documents
    # =====================
    @staticmethod
    def get_documents(db):

        documents = db.query(Document).all()

        return {
            "data": [
                {
                    "id": d.id,
                    "dossier_id": d.dossier_id,
                    "user_id": d.user_id,
                    "type_document": d.type_document,
                    "filename": d.filename,
                    "filepath": d.filepath,
                    "mime_type": d.mime_type
                }
                for d in documents
            ],
            "error": None
        }

    # =====================
    # DELETE DOCUMENT
    # =====================
    @staticmethod
    def delete_document(db, doc_id):

        document = db.query(Document).filter(Document.id == doc_id).first()

        if not document:
            return {"data": None, "error": "Document not found"}

        if document.filepath and os.path.exists(document.filepath):
            os.remove(document.filepath)

        db.delete(document)
        db.commit()

        return {
            "data": {"message": "Document deleted successfully"},
            "error": None
        }





