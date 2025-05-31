import hashlib

def calcular_md5(texto):
    """Calcula el hash MD5 de un texto y lo devuelve en hexadecimal."""
    return hashlib.md5(texto.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    while True:
        try:
            # Solicitar al usuario que ingrese un número
            numero_input = input("Ingresa el número para generar su hash MD5 (o escribe 'salir' para terminar): ")
            
            if numero_input.lower() == 'salir':
                print("Saliendo del generador de hashes.")
                break
            
            # No es necesario convertir a int si el ID es tratado como cadena directamente.
            # El input ya es una cadena, que es lo que necesitamos.
            # Si quisieras validar que es un número, podrías hacer: int(numero_input)
            # pero para el hash, usamos su representación como cadena.
            id_como_cadena = numero_input 
            
            # Calcular el hash MD5 del número (como cadena)
            hash_md5_generado = calcular_md5(id_como_cadena)
            
            print(f"El hash MD5 de la cadena '{id_como_cadena}' es: {hash_md5_generado}")
            print("-" * 30)
            
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número entero.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")