import requests

# URL desofuscada
base_url = "http://api-calculadora.softwareseguro.com.ar/verificar-codigo-calculadora/?t="

# Texto que deseas enviar como parámetro (puedes cambiarlo según sea necesario)
parametro = "ABCD"  # Ejemplo de texto o código

# Concatenar la URL con el parámetro
url_completa = base_url + parametro

try:
    # Realizar la petición GET
    respuesta = requests.get(url_completa)

    # Verificar el código de respuesta
    if respuesta.status_code == 200:
        print("Respuesta del servidor:")
        print(respuesta.text)
    else:
        print(f"Error en la petición. Código de estado: {respuesta.status_code}")
except Exception as e:
    print(f"Ocurrió un error: {e}")