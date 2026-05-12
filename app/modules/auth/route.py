from flask import Blueprint, request
from app.modules.auth.controller import AuthController
from app.core.security.decorators import login_required
from app.core.db import SessionLocal


auth_bp = Blueprint("auth", __name__)


# =====================
# LOGIN
# =====================
@auth_bp.route("/login", methods=["POST"])
def login():
    db = SessionLocal()
    try:
        data = request.get_json()
        return AuthController.login(data, db)
    finally:
        db.close()


# =====================
# REFRESH TOKEN
# =====================
@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    db = SessionLocal()
    try:
        auth_header = request.headers.get("Authorization")
        return AuthController.refresh(db, auth_header)
    finally:
        db.close()


# =====================
# LOGOUT
# =====================
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    return AuthController.logout()


# =====================
# CURRENT USER
# =====================
@auth_bp.route("/currentUser")
@login_required
def current_user():
    db = SessionLocal()
    try:
        return AuthController.current_user(db, request.user_id)
    finally:
        db.close()