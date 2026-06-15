from flask import jsonify, request
from app.core.db import SessionLocal
from app.modules.documents.service import DocumentService


class DocumentController:

    # =====================
    # CREATE DOCUMENT
    # =====================
    @staticmethod
    def create_document():

        db = SessionLocal()

        try:
            dossier_id = request.form.get("dossier_id")
            type_document = request.form.get("type_document")
            file = request.files.get("file")

            data = {
                "dossier_id": dossier_id,
                "type_document": type_document,
                "user_id": request.current_user["user_id"]
            }

            result = DocumentService.create_document(db, data, file)

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
    # GET DOCUMENT BY ID
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
            result = DocumentService.delete_document(db, doc_id)

            if result["error"]:
                return jsonify({"message": result["error"]}), 404

            return jsonify(result["data"]), 200

        finally:
            db.close()
