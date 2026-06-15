from flask import jsonify, request
from app.core.db import SessionLocal
from app.modules.vehicles.service import VehicleService


class VehicleController:

    # =====================
    # CREATE VEHICLE
    # =====================
    @staticmethod
    def create_vehicle():

        db = SessionLocal()

        try:
            data = request.form.to_dict() if request.form else request.get_json() or {}

            image = request.files.get("image")

            result = VehicleService.create_vehicle(db, data, image)

            if result["error"]:
                return jsonify({"message": result["error"]}), 400

            return jsonify({
                "message": "Vehicle created successfully",
                "data": result["data"]
            }), 201

        finally:
            db.close()

    # =====================
    # GET ALL VEHICLES
    # =====================
    @staticmethod
    def get_vehicles():

        db = SessionLocal()

        try:
            result = VehicleService.get_vehicles(db)

            return jsonify({
                "message": "Vehicles retrieved successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    # =====================
    # GET BY ID
    # =====================
    @staticmethod
    def get_vehicle_by_id(vehicle_id):

        db = SessionLocal()

        try:
            result = VehicleService.get_vehicle_by_id(db, vehicle_id)

            if result["error"]:
                return jsonify({"message": result["error"]}), 404

            return jsonify({
                "message": "Vehicle retrieved successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    # =====================
    # UPDATE VEHICLE
    # =====================
    @staticmethod
    def update_vehicle(vehicle_id):

        db = SessionLocal()

        try:
            data = request.form.to_dict() if request.form else request.get_json() or {}

            image = request.files.get("image")

            result = VehicleService.update_vehicle(db, vehicle_id, data, image)

            if result["error"]:
                return jsonify({"message": result["error"]}), 404

            return jsonify({
                "message": "Vehicle updated successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    # =====================
    # DELETE VEHICLE
    # =====================
    @staticmethod
    def delete_vehicle(vehicle_id):

        db = SessionLocal()

        try:
            result = VehicleService.delete_vehicle(db, vehicle_id)

            if result["error"]:
                return jsonify({"message": result["error"]}), 404

            return jsonify(result["data"]), 200

        finally:
            db.close()

    # =====================
    # AVAILABLE VEHICLES
    # =====================
    @staticmethod
    def get_available_vehicles():

        db = SessionLocal()

        try:
            vehicle_type = request.args.get("vehicle_type")

            result = VehicleService.get_available_vehicles(db, vehicle_type)

            return jsonify({
                "message": "Available vehicles retrieved successfully",
                "data": result["data"]
            }), 200

        finally:
            db.close()

    # =====================
    # SEARCH VEHICLES
    # =====================
    @staticmethod
    def search_vehicles():

        db = SessionLocal()

        try:
            filters = request.args.to_dict()

            result = VehicleService.search_vehicles(db, filters)

            return jsonify({
                "message": "Search completed successfully",
                "data": result["data"],
                "meta": result["meta"]
            }), 200

        finally:
            db.close()