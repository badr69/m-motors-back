from flask import Blueprint
from app.modules.documents.controller import DocumentController
from app.core.security.jwt_middleware import jwt_required
from app.core.security.decorators import require_role
import os
from flask import send_from_directory

documents_bp = Blueprint("documents", __name__,)


# =====================
# AUTH USER
# =====================

@documents_bp.route("", methods=["POST"])
@jwt_required
def create_document():
    return DocumentController.create_document()


@documents_bp.route("", methods=["GET"])
@jwt_required
def get_documents():
    return DocumentController.get_documents()


@documents_bp.route("/<int:doc_id>", methods=["GET"])
@jwt_required
def get_document_by_id(doc_id):
    return DocumentController.get_document_by_id(doc_id)


# =====================
# ADMIN ONLY
# =====================

@documents_bp.route("/<int:doc_id>", methods=["DELETE"])
@jwt_required
@require_role("ADMIN")
def delete_document(doc_id):
    return DocumentController.delete_document(doc_id)



@documents_bp.route("/file/<path:filename>")
def get_document_file(filename):

    upload_folder = os.path.abspath(
        os.path.join("uploads", "documents")
    )

    return send_from_directory(
        upload_folder,
        filename
    )