# vlan_range.py
# Script para clasificar rangos de VLAN

try:
    vlan = int(input("Ingrese el número de VLAN a consultar: "))

    if 1 <= vlan <= 1005:
        print(f"La VLAN {vlan} corresponde a un rango NORMAL.")
    elif 1006 <= vlan <= 4094:
        print(f"La VLAN {vlan} corresponde a un rango EXTENDIDO.")
    else:
        print(f"El número {vlan} NO corresponde a una VLAN respectiva.")

except ValueError:
    print("Error: Por favor, ingrese un número entero válido.")