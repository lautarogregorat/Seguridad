import requests

# URL de la API
url = "https://chl-0359de28-40ca-42a6-8cec-a9d8706a7330-notas-universitarias.softwareseguro.com.ar/home/"

# Cuerpo del POST
data = {
    "csrfmiddlewaretoken": "iIAsiGg9eGqJ9GDkBsvaCcWlEH5y5X8R",  # Token CSRF
    "materia_id": 7,  # ID de la materia
    "nota": 9  # Nota
}

# Encabezados de la solicitud
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Origin": "https://chl-0359de28-40ca-42a6-8cec-a9d8706a7330-notas-universitarias.softwareseguro.com.ar",
    "Referer": "https://chl-0359de28-40ca-42a6-8cec-a9d8706a7330-notas-universitarias.softwareseguro.com.ar/home/",
    "Sec-Ch-Ua": '"Not:A-Brand";v="24", "Chromium";v="134"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Upgrade-Insecure-Requests": "1",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "max-age=0",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i"
}

# Cookies de la solicitud
cookies = {
    "_ga": "GA1.3.752036958.1743859339",
    "_gid": "GA1.3.1809099391.1744068561",
    "sessionid": "hnbagss951qq4csp22mxfr3wx4l74azw",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MTYwMTYxLCJpYXQiOjE3NDQwNjQ0MDgsImp0aSI6IjE0MWY4M2M2NmYxYzRhNDQ4ZTM5NTdhYTg1MjJmZTE1IiwidXNlcl9pZCI6MzZ9.h6BDyL42YxusqvnLA2nY9S6YpUqDh_aheBsXopgPsFE",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6NDg2NjEzNzEwNSwiaWF0IjoxNzQ0MDczMTA1LCJqdGkiOiJkNGZmNTBmZmFkOWY0NzExODQyNzE4MjU2YTNiNTM4OCIsInVzZXJfaWQiOjI2fQ.PK6S8QgttIdgusAnEVV6IEfRjNxJVatrEWdNI3yiAVg",
    "csrftoken": "iIAsiGg9eGqJ9GDkBsvaCcWlEH5y5X8R"
}

# Realizar la solicitud POST
response = requests.post(url, data=data, headers=headers, cookies=cookies)

# Verificar el resultado
if response.status_code == 200:
    print("POST exitoso. Respuesta:")
    print(response.text)
else:
    print(f"Error en el POST. Código de estado: {response.status_code}")
    print(response.text)