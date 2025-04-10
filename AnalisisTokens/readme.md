# Análisis de Tokens Comprometidos

## Contexto

Recientemente, se detectó una filtración de tokens de acceso producto de un infostealer. Entre los tokens comprometidos, se encuentran tres pertenecientes a usuarios que estuvieron involucrados en ataques contra tu empresa.

Sabemos que estos tres tokens fueron firmados por Google, lo que te puede ayudar a identificarlos entre todos los demás.

**Nota:** Es probable que los tokens ya hayan expirado, pero analizarlos puede revelar los correos electrónicos de los atacantes.

## Solución Propuesta

El script `validarConGoogle.py` permite analizar un conjunto de tokens JWT para identificar aquellos que han expirado y extraer los correos electrónicos asociados. Esto se logra mediante los siguientes pasos:

1. **Obtención de claves públicas de Google:**  
   El script descarga las claves públicas desde el endpoint oficial de Google (`https://www.googleapis.com/oauth2/v3/certs`). Estas claves se utilizan para verificar la firma de los tokens.

2. **Lectura de tokens:**  
   Los tokens JWT se leen desde un archivo llamado `tokens.txt`, que debe estar ubicado en el mismo directorio que el script.

3. **Verificación y análisis de tokens:**  
   - Cada token se verifica utilizando las claves públicas de Google.
   - Si un token ha expirado, se decodifica sin verificar la firma para extraer el campo `email` del payload.

4. **Listado de correos electrónicos:**  
   Los correos electrónicos extraídos de los tokens expirados se ordenan alfabéticamente y se imprimen en la consola.

## Uso del Script

1. Coloca los tokens comprometidos en un archivo llamado `tokens.txt`, con un token por línea.
2. Ejecuta el script `validarConGoogle.py`:
   ```bash
   python validarConGoogle.py
   ```
3. El script mostrará en la consola los correos electrónicos asociados a los tokens expirados.

## Consideraciones

- El script maneja errores comunes, como la falta de conexión al endpoint de Google o la ausencia del archivo `tokens.txt`.
- Solo se procesan tokens firmados con el algoritmo `RS256`.
- Los correos electrónicos extraídos pueden ser útiles para identificar a los atacantes.

