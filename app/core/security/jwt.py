import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import Config


# =====================
# ACCESS TOKEN
# =====================
def generate_access_token(user):

    role = (user.role.name if user.role else "USER")
    role = role.upper().strip()

    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": role,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(
            hours=Config.JWT_EXPIRATION_HOURS
        )
    }

    print("[JWT DEBUG] access_token payload =", payload)

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

    print("[JWT DEBUG] refresh_token payload =", payload)

    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")


# =====================
# DECODE TOKEN (SAFE)
# =====================
def decode_token(token):

    try:
        payload = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=["HS256"]
        )

        print("[JWT DEBUG] decoded payload =", payload)

        return payload

    except jwt.ExpiredSignatureError:
        print("[JWT ERROR] token expired")
        return None

    except jwt.InvalidTokenError:
        print("[JWT ERROR] invalid token")
        return None