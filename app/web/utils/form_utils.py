import re
import secrets
import string

"""
    Comprueba si el formato de correo es correcto
"""
def is_valid_email(email: str) -> bool:
    regex = r"^\S+@\S+\.\S+$"
    return re.match(regex, email) is not None


