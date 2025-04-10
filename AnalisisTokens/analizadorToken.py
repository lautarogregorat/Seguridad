import jwt  # Asegúrate de instalar la biblioteca PyJWT: pip install pyjwt
import json

# Ruta del archivo que contiene los tokens JWT
ruta_archivo_token = "tokens.txt"

# Ruta del archivo donde se guardará la información decodificada
ruta_archivo_salida = "informacion_decodificada.json"

try:
    # Leer el contenido del archivo que contiene los tokens JWT
    with open(ruta_archivo_token, "r") as archivo:
        # Leer todas las líneas, eliminando espacios y saltos de línea adicionales
        lineas = archivo.readlines()
        tokens = [linea.strip() for linea in lineas if linea.strip()]  # Ignorar líneas vacías

    # Procesar cada token
    informacion_decodificada_total = []
    for token in tokens:
        try:
            # Decodificar el token JWT (sin verificar la firma)
            payload = jwt.decode(
                token,
                options={"verify_signature": False},
                algorithms=["RS256"]
            )

            # Agregar el token original al payload decodificado
            payload["raw_token"] = token  # Agregar el token original para referencia

            # Agregar el resultado a la lista total
            informacion_decodificada_total.append(payload)

        except jwt.InvalidTokenError:
            print(f"El token no es válido: {token}")
        except Exception as e:
            print(f"Ocurrió un error al procesar el token: {token}. Error: {e}")

    # Guardar la información decodificada en un archivo JSON
    with open(ruta_archivo_salida, "w") as archivo_salida:
        json.dump(informacion_decodificada_total, archivo_salida, indent=4)

    print(f"Información de tokens decodificados guardada en: {ruta_archivo_salida}")

except FileNotFoundError:
    print(f"No se encontró el archivo: {ruta_archivo_token}")
except Exception as e:
    print(f"Ocurrió un error: {e}")