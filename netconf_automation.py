# netconf_automation.py
# Script para automatizar la configuración del router CSR1000v usando NETCONF

from ncclient import manager
import xmltodict
import json

# Datos de conexión para el router CSR1000v en el laboratorio DEVASC
ROUTER_IP = "192.168.56.101"
ROUTER_PORT = 830  # Puerto estándar para NETCONF sobre SSH
USERNAME = "cisco"
PASSWORD = "cisco123!"

# 1. Plantilla XML para cambiar el Hostname (Debe llevar tu nombre y apellido)
xml_hostname = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>Juan_Correa_CSR1000v</hostname>
    </native>
</config>
"""

# 2. Plantilla XML para crear la interfaz Loopback 11 (IP 11.11.11.11/32)
xml_loopback = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback>
                <name>11</name>
                <description>Interfaz Loopback creada via NETCONF - Examen Devnet</description>
                <ip>
                    <address>
                        <primary>
                            <address>11.11.11.11</address>
                            <mask>255.255.255.255</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
    </native>
</config>
"""

def ejecutar_automatizacion():
    print("\n==================================================")
    print("   AUTOMATIZACIÓN CON NETCONF: ROUTER CSR1000v    ")
    print("==================================================")
    print(f"Conectando al dispositivo {ROUTER_IP}:{ROUTER_PORT}...")

    try:
        # Establecer la sesión NETCONF de forma segura
        with manager.connect(
            host=ROUTER_IP,
            port=ROUTER_PORT,
            username=USERNAME,
            password=PASSWORD,
            hostkey_verify=False,
            device_params={'name': 'iosxe'}
        ) as m:
            print("✅ Conexión NETCONF establecida con éxito.")
            
            # --- Tarea 1: Cambiar el Hostname ---
            print("\n[Tarea 1] Aplicando cambio de Hostname...")
            respuesta_hostname = m.edit_config(target='running', config=xml_hostname)
            if respuesta_hostname.ok:
                print(" -> ¡Hostname cambiado exitosamente a: Juan_Correa_CSR1000v!")
            
            # --- Tarea 2: Configurar Loopback 11 ---
            print("\n[Tarea 2] Configurando interfaz Loopback 11...")
            respuesta_loopback = m.edit_config(target='running', config=xml_loopback)
            if respuesta_loopback.ok:
                print(" -> ¡Interfaz Loopback 11 (11.11.11.11/32) creada exitosamente!")

            # --- Tarea 3: Verificar y mostrar la configuración actual ---
            print("\n[Tarea 3] Recuperando estado del Hostname desde el router...")
            filter_hostname = """
            <filter>
                <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                    <hostname/>
                </native>
            </filter>
            """
            config_xml = m.get_config(source='running', filter=filter_hostname).data_xml
            
            # Convertir XML a diccionario para mostrar una salida limpia en consola
            dict_datos = xmltodict.parse(config_xml)
            print("\n==================================================")
            print("         VERIFICACIÓN DE CAMBIOS EN DISPOSITIVO   ")
            print("==================================================")
            print(json.dumps(dict_datos, indent=4))
            print("==================================================")

    except Exception as e:
        print(f"❌ Error durante la conexión o configuración: {e}")

if __name__ == "__main__":
    ejecutar_automatizacion()