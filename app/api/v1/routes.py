from flask import Blueprint

# import tes modules
from app.modules.auth.route import auth_bp
from app.modules.roles.route import role_bp
from app.modules.users.routes import users_bp

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")


# =====================
# HEALTH CHECK
# =====================
@api_v1.route("/health")
def health():
    return {"status": "ok"}


# ===============
# REGISTER MODULES
# =====================
api_v1.register_blueprint(auth_bp, url_prefix="/auth")
api_v1.register_blueprint(role_bp, url_prefix="/roles")
api_v1.register_blueprint(users_bp, url_prefix="/users")
