import jwt
import json
import requests
from jwt.exceptions import ExpiredSignatureError

# Ruta del archivo que contiene los tokens JWT
ruta_archivo_token = "tokens.txt"

# Endpoint de Google para obtener las claves públicas
GOOGLE_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"

def obtener_claves_publicas_google():
    """Obtiene las claves públicas de Google desde el endpoint."""
    try:
        response = requests.get(GOOGLE_CERTS_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al obtener las claves públicas de Google: {e}")
        return None

def obtener_emails_expirados(tokens, claves_publicas):
    """Obtiene los emails de los tokens expirados."""
    emails_expirados = []
    for token in tokens:
        try:
            # Intentar verificar el token con cada clave pública
            for key in claves_publicas["keys"]:
                try:
                    jwt.decode(
                        token,
                        key=jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key)),
                        algorithms=["RS256"]
                    )
                except ExpiredSignatureError:
                    # Decodificar el token sin verificar la firma para extraer el email
                    payload = jwt.decode(
                        token,
                        options={"verify_signature": False},
                        algorithms=["RS256"]
                    )
                    email = payload.get("email")
                    if email:
                        emails_expirados.append(email)
                    break
        except Exception:
            continue
    return sorted(emails_expirados)

def main():
    try:
        # Leer el contenido del archivo que contiene los tokens JWT
        with open(ruta_archivo_token, "r") as archivo:
            tokens = [linea.strip() for linea in archivo if linea.strip()]

        # Obtener las claves públicas de Google
        claves_publicas = obtener_claves_publicas_google()
        if not claves_publicas:
            print("No se pudieron obtener las claves públicas de Google. Saliendo...")
            return

        # Obtener e imprimir los emails de los tokens expirados
        emails_expirados = obtener_emails_expirados(tokens, claves_publicas)
        print("Emails de tokens expirados (ordenados alfabéticamente):")
        for email in emails_expirados:
            print(email)

    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta_archivo_token}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()