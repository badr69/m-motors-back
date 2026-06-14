from flask import Blueprint
from app.modules.vehicles.controller import VehicleController
from app.core.security.jwt_middleware import jwt_required
from app.core.security.decorators import require_role

vehicle_bp = Blueprint("vehicles", __name__,)

# =====================
# PUBLIC (EPIC 3)
# =====================
@vehicle_bp.route("/search", methods=["GET"])
def search_vehicles():
    return VehicleController.search_vehicles()


@vehicle_bp.route("/available", methods=["GET"])
def get_available_vehicles():
    return VehicleController.get_available_vehicles()


@vehicle_bp.route("/<int:vehicle_id>", methods=["GET"])
def get_vehicle_by_id(vehicle_id):
    return VehicleController.get_vehicle_by_id(vehicle_id)


# =====================
# ADMIN ONLY (EPIC 2)
# =====================
@vehicle_bp.route("", methods=["POST"])
@jwt_required
@require_role("ADMIN")
def create_vehicle():
    return VehicleController.create_vehicle()


@vehicle_bp.route("/<int:vehicle_id>", methods=["PUT"])
@jwt_required
@require_role("ADMIN")
def update_vehicle(vehicle_id):
    return VehicleController.update_vehicle(vehicle_id)


@vehicle_bp.route("/<int:vehicle_id>", methods=["DELETE"])
@jwt_required
@require_role("ADMIN")
def delete_vehicle(vehicle_id):
    return VehicleController.delete_vehicle(vehicle_id)


@vehicle_bp.route("/<int:vehicle_id>/upload-image", methods=["POST"])
@jwt_required
@require_role("ADMIN")
def upload_vehicle_image(vehicle_id):
    return VehicleController.upload_vehicle_image(vehicle_id)


@vehicle_bp.route("/<int:vehicle_id>/image", methods=["PUT"])
@jwt_required
@require_role("ADMIN")
def update_vehicle_image(vehicle_id):
    return VehicleController.update_vehicle_image(vehicle_id)


@vehicle_bp.route("/<int:vehicle_id>/image", methods=["DELETE"])
@jwt_required
@require_role("ADMIN")
def delete_vehicle_image(vehicle_id):
    return VehicleController.delete_vehicle_image(vehicle_id)