from flask import jsonify, request
from app.core.db import SessionLocal
from app.modules.rental_dossiers.service import RentalDossierService


class RentalDossierController:

    # =====================
    # CREATE DOSSIER (US-12)
    # =====================
    @staticmethod
    def create_dossier():

        db = SessionLocal()

        try:
            data = request.get_json() or {}

            user_id = request.current_user["user_id"]

            result = RentalDossierService.create_dossier(
                db,
                user_id,
                data
            )

            if result["error"]:
                return jsonify({"message": result["error"]}), 400

            return jsonify({
                "message": "Dossier created successfully",
                "data": result["data"]
            }), 201

        finally:
            db.close()

    # =====================
    # US-15 - GET ALL DOSSIERS (ADMIN)
    # =====================
    @staticmethod
    def get_dossiers():

        db = SessionLocal()

        try:
            status = request.args.get("status")
            sort = request.args.get("sort", "desc")

            result = RentalDossierService.get_dossiers(
                db,
                status=status,
                sort=sort
            )

            return jsonify({
                "message": "Dossiers retrieved successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    @staticmethod
    def get_my_dossiers():

        db = SessionLocal()

        try:
            user_id = request.current_user["user_id"]

            result = RentalDossierService.get_my_dossiers(db, user_id)

            return jsonify({
                "message": "My dossiers retrieved successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()



    # =====================
    # GET BY ID
    # =====================
    @staticmethod
    def get_dossier_by_id(dossier_id):

        db = SessionLocal()

        try:
            user_id = request.current_user["user_id"]
            is_admin = request.current_user["role"] == "ADMIN"

            result = RentalDossierService.get_dossier_by_id(
                db,
                dossier_id,
                user_id,
                is_admin
            )

            if result["error"]:
                return jsonify({"message": result["error"]}), 404

            return jsonify({
                "message": "Dossier retrieved successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    # =====================
    # UPDATE STATUS (ADMIN)
    # =====================
    @staticmethod
    def update_status(dossier_id):

        db = SessionLocal()

        try:
            data = request.get_json() or {}

            result = RentalDossierService.update_status(
                db,
                dossier_id,
                data
            )

            if result["error"]:
                return jsonify({"message": result["error"]}), 400

            return jsonify({
                "message": "Dossier updated successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    # =====================
    # DELETE DOSSIER
    # =====================
    @staticmethod
    def delete_dossier(dossier_id):

        db = SessionLocal()

        try:
            user_id = request.current_user["user_id"]
            is_admin = request.current_user["role"] == "ADMIN"

            result = RentalDossierService.delete_dossier(
                db,
                dossier_id,
                user_id,
                is_admin
            )

            if result["error"]:
                return jsonify({"message": result["error"]}), 403

            return jsonify(result["data"]), 200

        finally:
            db.close()

