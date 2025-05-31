import hashlib

def calcular_md5(texto):
    """Calcula el hash MD5 de un texto y lo devuelve en hexadecimal."""
    return hashlib.md5(texto.encode('utf-8')).hexdigest()

# --- Script Modificado: Búsqueda con ID Incremental (sin salt explícito) ---

# --- Script para Analizar Lista de Tokens con MD5(id_string) ---

# Los 12 tokens que proporcionaste para lautig@yopmail.com
tokens_a_analizar = [
    "90e1357833654983612fb05e3ec9148c",
    "7ffd85d93a3e4de5c490d304ccd9f864",
    "d1e946f4e67db4b362ad23818a6fb78a",
    "6e79ed05baec2754e25b4eac73a332d2",
    "1f1baa5b8edac74eb4eaa329f14a0361",
    "5b6ba13f79129a74a3e819b78e36b922",
    "39027dfad5138c9ca0c474d71db915c3",
    "645098b086d2f9e1e0e939c27f9f2d6f",
    "faacbcd5bf1d018912c116bf2783e9a1",
    "09b15d48a1514d8209b192a8b8f34e48",
    "f542eae1949358e25d8bfeefe5b199f1",
    "f0bbac6fa079f1e00b2c14c1d3c6ccf0"
]

# También podemos añadir el token de utntest@yopmail.com si quieres analizarlo con esta lógica
# token_utntest = "c0a271bc0ecb776a094786474322cb82"
# tokens_a_analizar.append(token_utntest)

# Rango de IDs a probar para CADA token. 
# Ten cuidado, si el rango es muy grande y tienes muchos tokens, puede tardar.
rango_ids_min = 0
rango_ids_max = 5000 # Ajusta este valor según sea necesario

print(f"--- Iniciando Análisis de Lista de Tokens con MD5(id_string) ---")
print(f"Probando IDs desde {rango_ids_min} hasta {rango_ids_max} para cada token.\n")

for i, token_actual_de_lista in enumerate(tokens_a_analizar):
    print(f"Analizando token #{i+1}: {token_actual_de_lista}")
    encontrado_para_este_token = False
    id_exitoso = None
    input_exitoso = ""

    for id_valor_numerico in range(rango_ids_min, rango_ids_max + 1):
        id_actual_str = str(id_valor_numerico)
        
        texto_a_hashear = id_actual_str # Hipótesis: MD5(id_string)
        hash_generado = calcular_md5(texto_a_hashear)
        
        if hash_generado == token_actual_de_lista:
            encontrado_para_este_token = True
            id_exitoso = id_actual_str
            input_exitoso = texto_a_hashear
            print(f"  !!! ÉXITO para token {token_actual_de_lista} !!!")
            print(f"  ID encontrado: {id_exitoso}")
            print(f"  Input al MD5: '{input_exitoso}' (solo el ID)")
            print("-" * 30)
            break # Pasamos al siguiente token de la lista
    
    if not encontrado_para_este_token:
        print(f"  No se encontró un ID para el token {token_actual_de_lista} en el rango especificado.")
        print("-" * 30)

print("\n--- Análisis de Lista de Tokens Completado ---")