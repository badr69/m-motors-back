import os
import uuid

from flask import jsonify, request
from app.core.db import SessionLocal
from app.modules.documents.service import DocumentService
from app.core.security.extensions import ALLOWED_DOCUMENT_EXTENSIONS

UPLOAD_FOLDER = "uploads/documents"




def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_DOCUMENT_EXTENSIONS


class DocumentController:

    # =====================
    # CREATE DOCUMENT (UPLOAD FILE)
    # =====================
    @staticmethod
    def create_document():

        db = SessionLocal()

        try:
            # =====================
            # GET FORM DATA
            # =====================
            dossier_id = request.form.get("dossier_id")
            type_document = request.form.get("type_document")
            file = request.files.get("file")

            # =====================
            # VALIDATION FILE
            # =====================
            if not file or file.filename == "":
                return jsonify({"message": "No file provided"}), 400

            if not allowed_file(file.filename):
                return jsonify({"message": "File type not allowed"}), 400

            # =====================
            # SECURE FILENAME
            # =====================
            ext = file.filename.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4()}.{ext}"

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # =====================
            # SAVE IN DB
            # =====================
            data = {
                "dossier_id": dossier_id,
                # "user_id": request.user_id,
                "user_id": request.current_user["user_id"],# JWT middleware should inject user_id
                "type_document": type_document,
                "filename": file.filename,
                "filepath": filepath,
                "mime_type": file.mimetype
            }

            result = DocumentService.create_document(db, data)

            if result["error"]:
                return jsonify({"message": result["error"]}), 400

            return jsonify({
                "message": "Document uploaded successfully",
                "data": result["data"]
            }), 201

        finally:
            db.close()

    # =====================
    # GET ALL DOCUMENTS
    # =====================
    @staticmethod
    def get_documents():

        db = SessionLocal()

        try:
            result = DocumentService.get_documents(db)

            return jsonify({
                "message": "Documents retrieved successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    # =====================
    # GET BY ID
    # =====================
    @staticmethod
    def get_document_by_id(doc_id):

        db = SessionLocal()

        try:
            result = DocumentService.get_document_by_id(db, doc_id)

            if result["error"]:
                return jsonify({"message": result["error"]}), 404

            return jsonify({
                "message": "Document retrieved successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    # =====================
    # DELETE DOCUMENT
    # =====================

    @staticmethod
    def delete_document(doc_id):
        db = SessionLocal()

        try:
            # 1. fetch document (ORM inside service)
            result = DocumentService.get_document_by_id(db, doc_id)

            if result["error"]:
                return jsonify({"message": result["error"]}), 404

            document = result["data"]

            # 2. file deletion (OK controller-level)
            if document.get("filepath") and os.path.exists(document["filepath"]):
                os.remove(document["filepath"])

            # 3. delete DB (service handles ORM internally)
            result = DocumentService.delete_document(db, doc_id)

            return jsonify(result["data"]), 200

        finally:
            db.close()