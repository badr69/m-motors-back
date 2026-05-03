from werkzeug.security import generate_password_hash, check_password_hash


# =====================
# HASH PASSWORD
# =====================
def hash_password(password: str) -> str:
    return generate_password_hash(password)

# =====================
# VERIFY PASSWORD
# =====================
def verify_password(password: str, hashed_password: str) -> bool:
    return check_password_hash(hashed_password, password)