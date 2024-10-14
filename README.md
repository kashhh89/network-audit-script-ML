# Requisitos Previos #
Antes de ejecutar el script, asegúrate de tener lo siguiente:

Python 3.x instalado en tu sistema.    

Las siguientes bibliotecas de Python:   

netmiko   
PyYAML   

Acceso de red a los switches Cisco que deseas auditar.
Credenciales válidas (usuario y contraseña) para conectarte a los dispositivos vía SSH.

# Instalar las Bibliotecas Necesarias #
Abre una terminal en la carpeta del proyecto y ejecuta:

pip install netmiko pyyaml

Si usas macOS o Linux y el comando anterior no funciona, prueba con:

pip3 install netmiko pyyaml

# 3. Verificar la Instalación de Python # 

Asegúrate de que Python está instalado correctamente:

python --version

# Configuración #

1. Crear el archivo devices.yaml
   
El script utiliza un archivo devices.yaml para cargar la información de los switches. Debes crear este archivo en la carpeta del proyecto.
En tu editor de texto, crea un archivo llamado devices.yaml y agrega la siguiente estructura:

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

Asegúrate de reemplazar 192.168.1.x, tu_usuario y tu_contraseña con los datos reales de tus dispositivos.

Nota: Mantén la indentación correcta y utiliza espacios en lugar de tabulaciones. La indentación es crucial en archivos YAML.

# Ejecución del Script # 

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

Configuraciones de los switches: Archivos con el nombre <hostname>_config.txt que contienen la configuración de cada dispositivo.  

Archivo de Log: network_audit.log contiene registros de eventos, errores y violaciones detectadas.  

Reporte Final: reporte_final.txt incluye un resumen de los dispositivos que cumplen o no con los parámetros de seguridad y los cambios realizados.  

# Ver el Reporte Final # 

Abre reporte_final.txt para revisar:

Dispositivos que cumplen con los parámetros de seguridad.  
Dispositivos que requirieron actualizaciones.  
Detalles de los cambios aplicados.  

# Agregar Nuevos Dispositivos #

Para añadir más switches al script, simplemente edita el archivo devices.yaml y agrega más entradas siguiendo el formato existente.


# Agregar Nuevos Parámetros de Auditoría # 

Si deseas que el script verifique nuevos parámetros de seguridad, puedes modificar la función audit_configuration en el archivo network_audit.py.

Pasos para Agregar Nuevos Parámetros:

#1 - Abrir el archivo network_audit.py en tu editor de texto.

#2 - Localizar la función audit_configuration:

def audit_configuration(hostname, config):  
    violations = []    
    return violations  
    
#3- Añadir nuevas verificaciones:

Inserta tu nueva lógica de verificación dentro de esta función.  
Asegúrate de agregar cualquier violación detectada a la lista violations.

Ejemplo: Verificar si CDP está habilitado (y debería estar deshabilitado)

Verificar si CDP está habilitado   

if 'cdp run' in config:  
    violations.append('CDP está habilitado.')  
    
#4 Guardar los cambios y volver a ejecutar el script para que incluya las nuevas verificaciones.



# Gracias por utilizar este script! #
