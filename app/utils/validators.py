import re
from app.core.exceptions import ValidationException

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    if len(password) < 8:
        raise ValidationException("Password must be at least 8 characters long")
    return True

def validate_username(username: str) -> bool:
    if len(username) < 3:
        raise ValidationException("Username must be at least 3 characters long")
    return True
