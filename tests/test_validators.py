from app.core.validators import validate_email


# ======================
# VALID EMAIL
# ======================
def test_validate_email_valid():

    result = validate_email("test@test.com")

    assert result is None


# ======================
# INVALID EMAIL
# ======================
def test_validate_email_invalid():

    result = validate_email("bad-email")

    assert result == "Invalid email format"