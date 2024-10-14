Auditoría y Automatización de Configuraciones de Switches Cisco
Este script en Python automatiza la recolección, auditoría y actualización de configuraciones en switches Cisco. Conecta a múltiples dispositivos utilizando SSH, extrae sus configuraciones, verifica el cumplimiento de parámetros de seguridad y aplica cambios cuando es necesario.
Índice
•	Descripción General
•	Características
•	Requisitos Previos
•	Instalación
•	Configuración
o	1. Crear el archivo devices.yaml
o	2. Actualizar las credenciales y dispositivos
•	Ejecución del Script
•	Interpretación de Resultados
•	Agregar Nuevos Dispositivos
•	Agregar Nuevos Parámetros de Auditoría
•	Notas y Buenas Prácticas
•	Contacto
________________________________________
Descripción General
Este script está diseñado para facilitar la gestión y seguridad de una infraestructura de red compuesta por múltiples switches Cisco. Automatiza tareas repetitivas de administración y ayuda a garantizar el cumplimiento de estándares de seguridad al realizar auditorías y aplicar configuraciones necesarias.
Características
•	Recolección de Configuraciones: Conecta automáticamente a cada switch y descarga su configuración actual, guardándola en archivos separados.
•	Auditoría de Configuración: Revisa parámetros de seguridad clave, como la deshabilitación de Telnet, cifrado adecuado de contraseñas, configuración de NTP y asociación de listas de control de acceso en líneas VTY.
•	Aplicación de Configuraciones: Si se detectan violaciones, aplica automáticamente las configuraciones necesarias para corregirlas.
•	Reporte Final: Genera un informe detallado con los resultados de la auditoría y las acciones realizadas.
•	Manejo de Errores: Gestiona adecuadamente excepciones y errores de conexión o autenticación.

Requisitos Previos
Antes de ejecutar el script, asegúrate de tener lo siguiente:
•	Python 3.x instalado en tu sistema.
•	Las siguientes bibliotecas de Python:
o	netmiko
o	PyYAML
•	Acceso de red a los switches Cisco que deseas auditar.
•	Credenciales válidas (usuario y contraseña) para conectarte a los dispositivos vía SSH.
Instalación

1. Descargar el Repositorio
Descargar los archivos desde GitHub.
https://github.com/kashhh89/network-audit-script-ML

3. Instalar las Bibliotecas Necesarias
Abre una terminal en la carpeta del proyecto y ejecuta:
pip install netmiko pyyaml
Si usas macOS o Linux y el comando anterior no funciona, prueba con:
pip3 install netmiko pyyaml

5. Verificar la Instalación de Python
Asegúrate de que Python está instalado correctamente:
python --version
Deberías ver una respuesta como Python 3.x.x.

Configuración
1. Crear el archivo devices.yaml
El script utiliza un archivo devices.yaml para cargar la información de los switches. Debes crear este archivo en la carpeta del proyecto.
En tu editor de texto, crea un archivo llamado devices.yaml y agrega la siguiente estructura:
---
switches:
  - host: 192.168.1.1
    username: tu_usuario
    password: tu_contraseña
  - host: 192.168.1.2
    username: tu_usuario
    password: tu_contraseña
  - host: 192.168.1.3
    username: tu_usuario
    password: tu_contraseña
    
2. Actualizar las Credenciales y Dispositivos
•	host: La dirección IP o el nombre de host de cada switch.
•	username: El nombre de usuario para conectarte al switch.
•	password: La contraseña correspondiente.
Asegúrate de reemplazar IP, tu_usuario y tu_contraseña con los datos reales de tus dispositivos.
Nota: Mantén la indentación correcta y utiliza espacios en lugar de tabulaciones. La indentación es crucial en archivos YAML.

Ejecución del Script
1. Abrir una Terminal en la Carpeta del Proyecto
Navega hasta la carpeta donde se encuentra el script network_audit.py.
2. Ejecutar el Script
Ejecuta el siguiente comando:
python network_audit.py
Si usas macOS o Linux y el comando anterior no funciona, prueba con:
python3 network_audit.py
3. Observa la Ejecución
El script se conectará a cada switch listado en devices.yaml, extraerá su configuración, realizará la auditoría y aplicará cambios si es necesario.

Interpretación de Resultados

Después de la ejecución, se generarán los siguientes archivos:
•	Configuraciones de los switches: Archivos con el nombre <hostname>_config.txt que contienen la configuración de cada dispositivo.
•	Archivo de Log: network_audit.log contiene registros de eventos, errores y violaciones detectadas.
•	Reporte Final: reporte_final.txt incluye un resumen de los dispositivos que cumplen o no con los parámetros de seguridad y los cambios realizados.
Ver el Reporte Final
Abre reporte_final.txt para revisar:
•	Dispositivos que cumplen con los parámetros de seguridad.
•	Dispositivos que requirieron actualizaciones.
•	Detalles de los cambios aplicados.

Agregar Nuevos Dispositivos
Para añadir más switches al script, simplemente edita el archivo devices.yaml y agrega más entradas siguiendo el formato existente.
Ejemplo:

---
switches:
  - host: 192.168.1.1
    username: tu_usuario
    password: tu_contraseña
  - host: 192.168.1.2
    username: tu_usuario
    password: tu_contraseña
  - host: 192.168.1.3
    username: tu_usuario
    password: tu_contraseña
  - host: 192.168.1.4
    username: tu_usuario
    password: tu_contraseña
Recuerda: Mantén la indentación correcta y utiliza espacios en lugar de tabulaciones.

Agregar Nuevos Parámetros de Auditoría
Si deseas que el script verifique nuevos parámetros de seguridad, puedes modificar la función audit_configuration en el archivo network_audit.py.
Pasos para Agregar Nuevos Parámetros:
1.	Abrir el archivo network_audit.py en tu editor de texto.
2.	Localizar la función audit_configuration:

def audit_configuration(hostname, config):
    violations = []
    # Parámetros de auditoría existentes...
    return violations
    
3.	Añadir nuevas verificaciones:
o	Inserta tu nueva lógica de verificación dentro de esta función.
o	Asegúrate de agregar cualquier violación detectada a la lista violations.
Ejemplo: Verificar si CDP está habilitado (y debería estar deshabilitado)

# Verificar si CDP está habilitado
if 'cdp run' in config:
    violations.append('CDP está habilitado.')
    
4.	Guardar los cambios y volver a ejecutar el script para que incluya las nuevas verificaciones.
Aplicación de Configuraciones para Nuevos Parámetros
Si necesitas que el script aplique configuraciones para corregir las nuevas violaciones detectadas, debes:
1.	Modificar la función apply_new_configuration:
o	Agrega condiciones para verificar si la nueva violación está presente.
o	Añade los comandos necesarios a la lista config_commands.
Ejemplo: Deshabilitar CDP si está habilitado
python
Copy code
def apply_new_configuration(device, hostname, violations):
    config_applied = False
    config_commands = []
    try:
        connection = ConnectHandler(device_type='cisco_ios', **device)
        if 'CDP está habilitado.' in violations:
            config_commands.extend([
                'no cdp run'
            ])
            config_applied = True
        # Otros ajustes según violaciones detectadas
        if config_applied:
            connection.send_config_set(config_commands)
            logging.info(f'Se aplicaron configuraciones en {hostname} para corregir violaciones.')
        connection.disconnect()
        return config_applied
    except Exception as e:
        logging.error(f"Error al aplicar configuraciones en {hostname}: {e}")
        print(f"Error al aplicar configuraciones en {hostname}. Verifica los detalles en el archivo de log.")
        return False
2.	Guardar los cambios y ejecutar el script nuevamente.
Notas y Buenas Prácticas
•	Seguridad:
o	No compartas el archivo devices.yaml si contiene información sensible.
o	Asegúrate de que las credenciales y direcciones IP sean manejadas de forma segura.
•	Entorno de Pruebas:
o	Realiza pruebas en un entorno controlado antes de ejecutar el script en equipos de producción.
o	Verifica que los cambios aplicados no afecten negativamente la operación de la red.
•	Control de Versiones:
o	Usa un sistema de control de versiones como Git para mantener un historial de cambios en el script.
o	Excluye archivos sensibles en el archivo .gitignore.
•	Documentación:
o	Mantén comentarios en el código para facilitar futuras modificaciones.
o	Actualiza este archivo README.md si realizas cambios significativos.
•	Extensibilidad:
o	El script está diseñado de forma modular para facilitar la adición de nuevas funcionalidades.
o	Considera crear funciones separadas para tareas más complejas.

