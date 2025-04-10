import requests

# URL de la API
url = "https://chl-0359de28-40ca-42a6-8cec-a9d8706a7330-notas-universitarias.softwareseguro.com.ar/api/token/refresh/"

# Token de refresh bloqueado
refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6NDg2NjEyODQwOCwiaWF0IjoxNzQ0MDY0NDA4LCJqdGkiOiJhOTNmMmMxYWI0OTY0NGJiODY1OWMwOTI3ZmQwYmM1NCIsInVzZXJfaWQiOjM2fQ.MienEEx2ZuN-xdFj7Qti8HYXILlqZmVfjMhC-Hun_tw"

# Cuerpo del POST
data = {
    "refresh": refresh_token
}

# Encabezados de la solicitud
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

# Realizar la solicitud POST
response = requests.post(url, json=data, headers=headers)

# Verificar el resultado
if response.status_code == 200:
    print("Nuevo access token obtenido:")
    print(response.json())
else:
    print(f"Error en el POST. Código de estado: {response.status_code}")
   