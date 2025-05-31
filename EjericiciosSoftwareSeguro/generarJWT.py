import jwt

# Ingresar manualmente la clave secreta
secret_key = "123456@pz*+2p(e10(n7891"

# Datos para el payload del JWT
payload = {
    "user_id": 1,
    "username": "administrador_multas@yopmail.com",
    "exp": 1744485748,  # Fecha de expiración en formato UNIX
    "email": "administrador_multas@yopmail.com",
    "orig_iat": 1743880948  # Fecha de emisión en formato UNIX
}

# Generar el JWT
token = jwt.encode(payload, secret_key, algorithm="HS256")
print(f"JWT generado: {token}")