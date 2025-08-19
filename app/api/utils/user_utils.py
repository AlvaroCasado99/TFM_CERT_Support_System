import secrets
import string

"""
    Devuelve una contraseña aleatoria conforme a las normas NIST
"""
def generate_nist_password(length: int = 12) -> str:

    if length < 8:
        raise ValueError("La contraseña debe tener mínimo 8 caracteres")

    # Formar alfabeto
    alfabeto = string.ascii_letters + string.digits + string.punctuation

    # Generar contraseña aleatoria
    password = ''.join(secrets.choice(alfabeto) for _ in range(length))
    
    return password
