from flask import Blueprint

# import tes modules
from app.modules.auth.route import auth_bp
from app.modules.documents.routes import documents_bp
from app.modules.rental_dossiers.routes import rental_dossier_bp
from app.modules.roles.route import role_bp
from app.modules.users.routes import user_bp
from app.modules.vehicles.routes import vehicle_bp

api_v1 = Blueprint("api_v1", __name__,)


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
api_v1.register_blueprint(user_bp, url_prefix="/users")
api_v1.register_blueprint(vehicle_bp, url_prefix="/vehicles")
api_v1.register_blueprint(rental_dossier_bp, url_prefix="/rental_dossiers")
api_v1.register_blueprint(documents_bp, url_prefix="/documents")
