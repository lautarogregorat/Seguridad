import requests
from concurrent.futures import ThreadPoolExecutor
import hashlib

# URL base
url_base = "https://chl-a2aff19c-43e7-48ad-8a6f-9daa078ab420-ventas.softwareseguro.com.ar/ventas/?id="

# Cabeceras comunes
headers = {
    "Host": "chl-a2aff19c-43e7-48ad-8a6f-9daa078ab420-ventas.softwareseguro.com.ar",
    "Cookie": "_ga=GA1.3.752036958.1743859339; _gid=GA1.3.151983393.1743859339",
    "Sec-Ch-Ua": "\"Not:A-Brand\";v=\"24\", \"Chromium\";v=\"134\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Accept-Language": "es-ES,es;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i"
}

# Contador global para respuestas 403
contador_403 = 0

# Función para realizar una solicitud
def realizar_peticion(id):
    global contador_403
    url = f"{url_base}{id}"
    try:
        response = requests.get(url, headers=headers)
        print(f"ID {id}: Código de estado {response.status_code}")
        
        if response.status_code == 403:
            contador_403 += 1
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud para el ID {id}: {e}")

# Usar ThreadPoolExecutor para realizar solicitudes en paralelo
with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(realizar_peticion, range(0, 3001))

# Convertir el contador a hash MD5
contador_403_str = str(contador_403)
hash_md5 = hashlib.md5(contador_403_str.encode()).hexdigest()

# Resultados
print(f"Total de respuestas 403: {contador_403}")
print(f"Hash MD5 del contador: {hash_md5}")