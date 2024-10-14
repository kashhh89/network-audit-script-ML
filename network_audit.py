from netmiko import ConnectHandler
import yaml
import logging

# Configurar el registro (Logging)
logging.basicConfig(filename='network_audit.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Función para cargar los dispositivos desde un archivo YAML
def load_devices(file_path):
    with open(file_path, 'r') as file:
        devices = yaml.safe_load(file)
    return devices['switches']

# Función para conectarse y extraer la configuración de un dispositivo
def collect_configuration(device):
    try:
        connection = ConnectHandler(device_type='cisco_ios', **device)
        hostname = connection.send_command('show run | include hostname').split()[1]
        config = connection.send_command('show running-config')
        # Guardar la configuración en un archivo
        with open(f'{hostname}_config.txt', 'w') as config_file:
            config_file.write(config)
        connection.disconnect()
        return hostname, config
    except Exception as e:
        logging.error(f"Error al conectar con {device['host']}: {e}")
        print(f"Error al conectar con {device['host']}. Verifica los detalles en el archivo de log.")
        return None, None

# Función para auditar la configuración de un dispositivo
def audit_configuration(hostname, config):
    violations = []

    # Verificar si Telnet está habilitado
    if 'transport input telnet' in config:
        violations.append('Telnet está habilitado.')

    # Verificar cifrado de contraseñas (buscamos 'password 7' o 'enable secret')
    if 'password 7 ' in config or 'enable secret' not in config:
        violations.append('Las contraseñas no están correctamente cifradas.')

    # Verificar configuración de NTP y autenticación
    if 'ntp server' not in config or 'ntp authenticate' not in config:
        violations.append('NTP no está configurado correctamente o falta autenticación.')

    # Verificar si line vty tiene una ACL asociada
    lines = config.splitlines()
    vty_section = False
    acl_associated = False
    for line in lines:
        if line.strip().startswith('line vty'):
            vty_section = True
        elif vty_section and 'access-class' in line:
            acl_associated = True
            break
        elif vty_section and line.startswith('!'):
            vty_section = False

    if not acl_associated:
        violations.append('Line vty no tiene una ACL asociada.')

    # Registrar las violaciones
    if violations:
        logging.info(f'Violaciones en {hostname}: {", ".join(violations)}')
    return violations

# Función para aplicar nuevas configuraciones en caso de violaciones
def apply_new_configuration(device, hostname, violations):
    # Solo aplicaremos configuraciones si Telnet está habilitado
    if 'Telnet está habilitado.' in violations:
        try:
            connection = ConnectHandler(device_type='cisco_ios', **device)
            config_commands = [
                'configure terminal',
                'line vty 0 4',
                'transport input ssh',
                'exit',
                'ip domain-name example.com',
                'crypto key generate rsa modulus 1024',
                'ip ssh version 2',
                'exit'
            ]
            connection.send_config_set(config_commands)
            logging.info(f'Se aplicaron configuraciones en {hostname} para deshabilitar Telnet y habilitar SSH.')
            connection.disconnect()
            return True
        except Exception as e:
            logging.error(f"Error al aplicar configuraciones en {hostname}: {e}")
            print(f"Error al aplicar configuraciones en {hostname}. Verifica los detalles en el archivo de log.")
            return False
    return False

# Función principal
def main():
    devices = load_devices('devices.yaml')
    compliant_devices = []
    updated_devices = []
    changes_made = {}

    for device in devices:
        hostname, config = collect_configuration(device)
        if hostname and config:
            violations = audit_configuration(hostname, config)
            if violations:
                config_applied = apply_new_configuration(device, hostname, violations)
                if config_applied:
                    updated_devices.append(hostname)
                    changes_made[hostname] = 'Deshabilitado Telnet y habilitado SSH.'
            else:
                compliant_devices.append(hostname)

    # Generar el reporte final
    with open('reporte_final.txt', 'w') as report_file:
        report_file.write('Reporte de Auditoría de Red\n')
        report_file.write('===========================\n\n')
        report_file.write('Dispositivos que cumplen con los parámetros de seguridad:\n')
        for device in compliant_devices:
            report_file.write(f'- {device}\n')
        report_file.write('\nDispositivos que requirieron una actualización de configuración:\n')
        for device in updated_devices:
            report_file.write(f'- {device}\n')
        report_file.write('\nDetalles de los cambios realizados:\n')
        for device, change in changes_made.items():
            report_file.write(f'- {device}: {change}\n')

if __name__ == '__main__':
    main()
