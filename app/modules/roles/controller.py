from flask import jsonify, request
from app.core.db import SessionLocal
from app.modules.roles.service import RoleService


class RoleController:

    @staticmethod
    def create_role():
        db = SessionLocal()
        try:
            data = request.get_json() or {}
            result = RoleService.create_role(db, data.get("name"))

            if result.get("error"):
                return jsonify(result), 400

            return jsonify(result), 201

        finally:
            db.close()

    @staticmethod
    def get_all():
        db = SessionLocal()
        try:
            result = RoleService.get_roles(db)
            return jsonify(result), 200
        finally:
            db.close()

    @staticmethod
    def get_one(role_id):
        db = SessionLocal()
        try:
            result = RoleService.get_role_by_id(db, role_id)

            if result.get("error"):
                return jsonify(result), 404

            return jsonify(result), 200

        finally:
            db.close()

    @staticmethod
    def update(role_id):
        db = SessionLocal()
        try:
            data = request.get_json() or {}
            result = RoleService.update_role(db, role_id, data)

            if result.get("error"):
                return jsonify(result), 400

            return jsonify(result), 200

        finally:
            db.close()

    @staticmethod
    def delete(role_id):
        db = SessionLocal()
        try:
            result = RoleService.delete_role(db, role_id)

            if result.get("error"):
                return jsonify(result), 404

            return jsonify(result), 200

        finally:
            db.close()