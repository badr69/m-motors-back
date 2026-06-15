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

        if not file or file.filename == "":
            return {"data": None, "error": "No file provided"}

        if not allowed_file(file.filename):
            return {"data": None, "error": "File type not allowed"}

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        file.save(filepath)

        # =====================
        # ORM OBJECT (FIX MAJEUR)
        # =====================
        document = Document(
            dossier_id=data.get("dossier_id"),
            user_id=data.get("user_id"),
            type_document=data.get("type_document"),
            filename=filename,
            filepath=filepath,
            mime_type=file.mimetype
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
                "mime_type": document.mime_type
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
                    "mime_type": d.mime_type
                }
                for d in documents
            ],
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






# import os
# import uuid
# from app.core.security.extensions import ALLOWED_DOCUMENT_EXTENSIONS
#
#
# UPLOAD_FOLDER = "uploads/documents"
#
#
# def allowed_file(filename):
#     return (
#         "." in filename
#         and filename.rsplit(".", 1)[1].lower() in ALLOWED_DOCUMENT_EXTENSIONS
#     )
#
#
# class DocumentService:
#
#     # =====================
#     # CREATE DOCUMENT
#     # =====================
#     @staticmethod
#     def create_document(db, data, file):
#
#         # =====================
#         # VALIDATION FILE
#         # =====================
#         if not file or file.filename == "":
#             return {
#                 "data": None,
#                 "error": "No file provided"
#             }
#
#         if not allowed_file(file.filename):
#             return {
#                 "data": None,
#                 "error": "File type not allowed"
#             }
#
#         # =====================
#         # PREPARE UPLOAD FOLDER
#         # =====================
#         os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#
#         # =====================
#         # SECURE FILE NAME
#         # =====================
#         ext = file.filename.rsplit(".", 1)[1].lower()
#         filename = f"{uuid.uuid4()}.{ext}"
#
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#
#         # =====================
#         # SAVE FILE ON DISK
#         # =====================
#         file.save(filepath)
#
#         # =====================
#         # BUILD DOCUMENT DATA
#         # =====================
#         document_data = {
#             "dossier_id": data.get("dossier_id"),
#             "user_id": data.get("user_id"),
#             "type_document": data.get("type_document"),
#             "filename": file.filename,
#             "filepath": filepath,
#             "mime_type": file.mimetype
#         }
#
#         # =====================
#         # SAVE IN DB
#         # =====================
#         document = db.add(document_data)
#
#         return {
#             "data": document_data,
#             "error": None
#         }
#
#     # =====================
#     # GET ALL DOCUMENTS
#     # =====================
#     @staticmethod
#     def get_documents(db):
#
#         documents = db.query().all()
#
#         return {
#             "data": documents,
#             "error": None
#         }
#
#     # =====================
#     # GET DOCUMENT BY ID
#     # =====================
#     @staticmethod
#     def get_document_by_id(db, doc_id):
#
#         document = db.query().filter_by(id=doc_id).first()
#
#         if not document:
#             return {
#                 "data": None,
#                 "error": "Document not found"
#             }
#
#         return {
#             "data": document,
#             "error": None
#         }
#
#     # =====================
#     # DELETE DOCUMENT
#     # =====================
#     @staticmethod
#     def delete_document(db, doc_id):
#
#         document = db.query().filter_by(id=doc_id).first()
#
#         if not document:
#             return {
#                 "data": None,
#                 "error": "Document not found"
#             }
#
#         # =====================
#         # DELETE FILE FROM DISK
#         # =====================
#         if document.get("filepath") and os.path.exists(document["filepath"]):
#             os.remove(document["filepath"])
#
#         # =====================
#         # DELETE FROM DB
#         # =====================
#         db.delete(document)
#         db.commit()
#
#         return {
#             "data": {
#                 "message": "Document deleted successfully"
#             },
#             "error": None
#         }