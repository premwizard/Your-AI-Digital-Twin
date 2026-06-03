from typing import Dict, List


def validate_register_payload(payload: Dict) -> List[str]:
    errors = []
    if not payload.get("email"):
        errors.append("email is required")
    if not payload.get("password"):
        errors.append("password is required")
    if not payload.get("username"):
        errors.append("username is required")
    return errors


def validate_login_payload(payload: Dict) -> List[str]:
    errors = []
    if not payload.get("email"):
        errors.append("email is required")
    if not payload.get("password"):
        errors.append("password is required")
    return errors
