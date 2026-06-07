from typing import Optional, Dict, Any
import re


# =====================
# EMAIL VALIDATION
# =====================
def validate_email(email: Optional[str]) -> Optional[str]:

    if not email:
        return "Email is required"

    email = str(email).strip()

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(email_regex, email):
        return "Invalid email format"

    return None


# =====================
# PASSWORD VALIDATION
# =====================
def validate_password(password: Optional[str]) -> Optional[str]:

    if not password:
        return "Password is required"

    password = str(password)

    if len(password) < 6:
        return "Password must be at least 6 characters"

    if len(password) > 100:
        return "Password too long"

    return None


# =====================
# USERNAME VALIDATION
# =====================
def validate_username(username: Optional[str]) -> Optional[str]:

    if not username:
        return "Username is required"

    username = str(username).strip()

    if len(username) < 3:
        return "Username must be at least 3 characters"

    if len(username) > 50:
        return "Username too long"

    return None


# =====================
# LOGIN VALIDATION
# =====================
def validate_login(data: Dict[str, Any]) -> Optional[str]:

    email_error = validate_email(data.get("email"))
    if email_error:
        return email_error

    password_error = validate_password(data.get("password"))
    if password_error:
        return password_error

    return None


# =====================
# REGISTER VALIDATION
# =====================
def validate_register(data: Dict[str, Any]) -> Optional[str]:

    username_error = validate_username(data.get("username"))
    if username_error:
        return username_error

    email_error = validate_email(data.get("email"))
    if email_error:
        return email_error

    password_error = validate_password(data.get("password"))
    if password_error:
        return password_error

    return None


# =====================
# REQUIRED FIELD VALIDATION (GENERIC)
# =====================
def validate_required(value: Optional[str], field_name: str) -> Optional[str]:

    if not value:
        return f"{field_name} is required"

    return None