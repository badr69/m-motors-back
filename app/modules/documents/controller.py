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
            data = request.get_json() or {}

            result = DocumentService.create_document(db, data)

            if result["error"]:
                return jsonify({"message": result["error"]}), 400

            return jsonify({
                "message": "Document created successfully",
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
            result = DocumentService.delete_document(db, doc_id)

            if result["error"]:
                return jsonify({"message": result["error"]}), 404

            return jsonify(result["data"]), 200

        finally:
            db.close()