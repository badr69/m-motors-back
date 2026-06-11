from app.modules.documents.model import Document
from typing import Dict, Any


class DocumentService:

    # =====================
    # CREATE DOCUMENT (UPLOAD)
    # =====================
    @staticmethod
    def create_document(db, data: Dict[str, Any]):

        allowed_types = ["identity", "domicile", "revenu", "rib"]

        allowed_mime_types = [
            "application/pdf",
            "image/jpeg",
            "image/png"
        ]

        # =====================
        # VALIDATION TYPE
        # =====================
        if data.get("type_document") not in allowed_types:
            return {
                "data": None,
                "error": "Invalid document type"
            }

        # =====================
        # VALIDATION MIME TYPE
        # =====================
        if data.get("mime_type") not in allowed_mime_types:
            return {
                "data": None,
                "error": "Invalid file type"
            }

        document = Document(
            dossier_id=data.get("dossier_id"),
            user_id=data.get("user_id"),
            type_document=data.get("type_document"),
            filename=data.get("filename"),
            filepath=data.get("filepath"),
            mime_type=data.get("mime_type")
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return {
            "data": {
                "id": document.id,
                "dossier_id": document.dossier_id,
                "user_id": document.user_id,
                "type_document": document.type_document,
                "filename": document.filename,
                "filepath": document.filepath,
                "mime_type": document.mime_type,
                "created_at": document.created_at
            },
            "error": None
        }

    # =====================
    # GET ALL DOCUMENTS
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
                    "mime_type": d.mime_type,
                    "created_at": d.created_at
                }
                for d in documents
            ],
            "error": None
        }

    # =====================
    # GET DOCUMENT BY ID
    # =====================
    @staticmethod
    def get_document_by_id(db, doc_id: int):

        document = db.query(Document).filter(
            Document.id == doc_id
        ).first()

        if not document:
            return {
                "data": None,
                "error": "Document not found"
            }

        return {
            "data": {
                "id": document.id,
                "dossier_id": document.dossier_id,
                "user_id": document.user_id,
                "type_document": document.type_document,
                "filename": document.filename,
                "filepath": document.filepath,
                "mime_type": document.mime_type,
                "created_at": document.created_at
            },
            "error": None
        }

    # =====================
    # DELETE DOCUMENT (EPIC RULE)
    # =====================
    @staticmethod
    def delete_document(db, doc_id):

        document = db.query(Document).filter(Document.id == doc_id).first()

        if not document:
            return {"data": None, "error": "Document not found"}

        db.delete(document)
        db.commit()

        return {
            "data": {
                "message": "Document deleted successfully"
            },
            "error": None
        }