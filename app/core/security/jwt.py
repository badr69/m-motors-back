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
        "role": (user.role.name if user.role else "CLIENT").upper(),
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
# DECODE TOKEN (CLEAN + SAFE)
# =====================
def decode_token(token, expected_type=None):

    try:
        payload = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=["HS256"]
        )

        # =====================
        # TYPE VALIDATION
        # =====================
        if expected_type and payload.get("type") != expected_type:
            return None

        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None

    except Exception:
        return None