# Análisis de Tokens Comprometidos

## Contexto

Recientemente, se detectó una filtración de tokens de acceso producto de un infostealer. Entre los tokens comprometidos, se encuentran tres pertenecientes a usuarios que estuvieron involucrados en ataques contra tu empresa.

Sabemos que estos tres tokens fueron firmados por Google, lo que te puede ayudar a identificarlos entre todos los demás.

**Nota:** Es probable que los tokens ya hayan expirado, pero analizarlos puede revelar los correos electrónicos de los atacantes.

---

## 🔐 ¿Por qué se usa una clave pública?

Cuando Google emite un token JWT (por ejemplo, en una autenticación OAuth2), lo firma digitalmente con una clave privada que solo ellos tienen.  
Para comprobar que el token realmente fue emitido por Google y que no fue alterado, cualquiera puede usar la clave pública correspondiente para verificar esa firma.

---

## 📥 Paso a paso de cómo se valida el token

### 1. Obtener las claves públicas de Google

Google publica sus claves públicas en este endpoint:  
`https://www.googleapis.com/oauth2/v3/certs`

El JSON obtenido contiene varias claves (en formato JWK), cada una con un `kid` (Key ID).  
Ejemplo parcial:

```json
{
  "keys": [
    {
      "kid": "abcdef123456...",
      "alg": "RS256",
      "n": "...",
      "e": "AQAB",
      "kty": "RSA",
      "use": "sig"
    },
    ...
  ]
}
```

### 2. Leer el token JWT

Un JWT tiene esta estructura:  
`HEADER.PAYLOAD.SIGNATURE`

En el `HEADER` (codificado en base64) hay algo como esto:

```json
{
  "alg": "RS256",
  "kid": "abcdef123456..."
}
```

El `kid` indica cuál clave pública de la lista debe usarse para verificar este token.

### 3. Verificar el token con la clave pública

Usando una librería como `jwt` en Python (PyJWT) o alguna en tu lenguaje preferido, el proceso general es:

```python
jwt.decode(token, key=clave_publica, algorithms=["RS256"], audience="tu_client_id")
```

El módulo recalcula la firma del `header` + `payload` usando la clave pública y la compara con la parte `SIGNATURE` del token.  
Si coinciden y el token no ha expirado, es válido ✅.

### 4. ¿Y si el token está expirado?

Cuando un token ha expirado, la verificación con `jwt.decode(..., verify=True)` falla.  
En ese caso, se puede hacer:

```python
jwt.decode(token, options={"verify_signature": False})
```

Esto omite la verificación de firma y expiración, permitiéndote inspeccionar el `payload` para extraer, por ejemplo, el email:

```json
{
  "email": "usuario@gmail.com",
  "exp": 1700000000,
  ...
}
```

---

## Solución Propuesta

El script `validarConGoogle.py` permite analizar un conjunto de tokens JWT para identificar aquellos que han expirado y extraer los correos electrónicos asociados. Esto se logra mediante los siguientes pasos:

1. **Obtención de claves públicas de Google:**  
   El script descarga las claves públicas desde el endpoint oficial de Google (`https://www.googleapis.com/oauth2/v3/certs`). Estas claves se utilizan para verificar la firma de los tokens.

2. **Lectura de tokens:**  
   Los tokens JWT se leen desde un archivo llamado `tokens.txt`, que debe estar ubicado en el mismo directorio que el script.

3. **Verificación y análisis de tokens:**  
   - Cada token se verifica utilizando las claves públicas de Google.
   - Si un token ha expirado, se decodifica sin verificar la firma para extraer el campo `email` del payload.
   - Si ninguna clave pública valida la firma del token (ya sea por estar equivocada, ser de otro issuer, o estar corrupta), ese token se ignora completamente y su email no se extrae, ni siquiera si está expirado.

4. **Listado de correos electrónicos:**  
   Los correos electrónicos extraídos de los tokens expirados se ordenan alfabéticamente y se imprimen en la consola.

---

## Uso del Script

1. Coloca los tokens comprometidos en un archivo llamado `tokens.txt`, con un token por línea.
2. Ejecuta el script `validarConGoogle.py`:
   ```bash
   python validarConGoogle.py
   ```
3. El script mostrará en la consola los correos electrónicos asociados a los tokens expirados.

---

## 🛡️ ¿Para qué sirve esto en la práctica?

- Confirmar que el token es legítimo (no fue alterado ni falsificado).
- Verificar que está vigente.
- Extraer la identidad del usuario autenticado (por ejemplo, su email).

---

## Consideraciones

- El script maneja errores comunes, como la falta de conexión al endpoint de Google o la ausencia del archivo `tokens.txt`.
- Solo se procesan tokens firmados con el algoritmo `RS256`.
- Los correos electrónicos extraídos pueden ser útiles para identificar a los atacantes.

