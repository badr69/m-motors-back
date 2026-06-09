from flask import Blueprint
from app.modules.rental_dossiers.controller import RentalDossierController
from app.core.security.jwt_middleware import jwt_required
from app.core.security.decorators import require_role

rental_dossier_bp = Blueprint("rental_dossiers", __name__)

# =====================
# CLIENT (US-12 / US-13)
# =====================

@rental_dossier_bp.route("", methods=["POST"])
@jwt_required
def create_dossier():
    return RentalDossierController.create_dossier()


# =====================
# ADMIN ONLY
# =====================
@rental_dossier_bp.route("", methods=["GET"])
@jwt_required
@require_role("ADMIN")
def get_dossiers():
    return RentalDossierController.get_dossiers()


@rental_dossier_bp.route("/my", methods=["GET"])
@jwt_required
def get_my_dossiers():
    return RentalDossierController.get_my_dossiers()


@rental_dossier_bp.route("/<int:dossier_id>", methods=["GET"])
@jwt_required
def get_dossier_by_id(dossier_id):
    return RentalDossierController.get_dossier_by_id(dossier_id)


@rental_dossier_bp.route("/<int:dossier_id>/cancel", methods=["PATCH"])
@jwt_required
def cancel_dossier(dossier_id):
    return RentalDossierController.cancel_dossier(dossier_id)


@rental_dossier_bp.route("/<int:dossier_id>", methods=["DELETE"])
@jwt_required
def delete_dossier(dossier_id):
    return RentalDossierController.delete_dossier(dossier_id)







@rental_dossier_bp.route("/<int:dossier_id>", methods=["PATCH"])
@jwt_required
@require_role("ADMIN")
def update_status(dossier_id):
    return RentalDossierController.update_status(dossier_id)