import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import Config


# =====================
# ACCESS TOKEN
# =====================
def generate_access_token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,

        # sécurité : éviter crash si role null
        "role": user.role.name if user.role else "USER",

        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(
            hours=Config.JWT_EXPIRATION_HOURS
        )
    }

    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")


# =====================
# REFRESH TOKEN
# =====================
def generate_refresh_token(user):
    payload = {
        "user_id": user.id,
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }

    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")


# =====================
# DECODE TOKEN
# =====================
def decode_token(token):
    return jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])