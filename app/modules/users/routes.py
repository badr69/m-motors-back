from flask import Blueprint, request
from app.modules.users.controller import UserController
from app.core.db import SessionLocal
from app.core.security.decorators import login_required, admin_required

users_bp = Blueprint("users", __name__)


# =====================
# CREATE USER (ADMIN ONLY)
# =====================
@users_bp.route("", methods=["POST"])
@login_required
@admin_required
def create_user():

    db = SessionLocal()
    try:
        return UserController.create(request.get_json(), db)
    finally:
        db.close()


# =====================
# GET ALL USERS (ADMIN ONLY)
# =====================
@users_bp.route("", methods=["GET"])
@login_required
@admin_required
def get_users():

    db = SessionLocal()
    try:
        return UserController.get_all(db)
    finally:
        db.close()


# =====================
# GET ONE USER (ADMIN OR OWNER)
# =====================
@users_bp.route("/<int:user_id>", methods=["GET"])
@login_required
def get_user(user_id):

    db = SessionLocal()
    try:
        return UserController.get_one(user_id, db)
    finally:
        db.close()


# =====================
# UPDATE USER (ADMIN OR OWNER)
# =====================
@users_bp.route("/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id):

    db = SessionLocal()
    try:
        return UserController.update(user_id, request.get_json(), db)
    finally:
        db.close()


# =====================
# DELETE USER (ADMIN ONLY)
# =====================
@users_bp.route("/<int:user_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_user(user_id):

    db = SessionLocal()
    try:
        return UserController.delete(user_id, db)
    finally:
        db.close()