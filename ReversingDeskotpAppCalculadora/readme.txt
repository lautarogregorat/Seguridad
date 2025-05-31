# Reversing Desktop App - Calculadora

## Descripción
Este proyecto consiste en una aplicación de escritorio que simula una calculadora. Durante el análisis de reversing, se identificó un string ofuscado que contenía una URL. Este string fue desofuscado para obtener la URL real, y se realizaron peticiones HTTP enviando parámetros específicos.

## Proceso de Reversing
1. **Identificación del string ofuscado**: En el código fuente de la aplicación, se encontró un string codificado en Base64.
2. **Desofuscación**: Se utilizó la función `Base64.getDecoder().decode()` para desofuscar el string y obtener la URL original.
3. **Peticiones HTTP**: Con la URL desofuscada, se realizaron peticiones GET enviando parámetros como `ABCD` para analizar la respuesta del servidor.

## Ejecución de la Petición
El archivo `peticion.py` contiene un ejemplo de cómo se realiza una petición HTTP a la URL desofuscada con el parámetro `ABCD`. Este script utiliza la biblioteca `requests` de Python para enviar la solicitud y manejar la respuesta.

## Notas
- Este proyecto tiene fines educativos y de análisis de reversing.
- No se debe utilizar para actividades malintencionadas.

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
