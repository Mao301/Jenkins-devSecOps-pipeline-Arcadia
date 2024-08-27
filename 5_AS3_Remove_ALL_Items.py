import requests
import json
from requests.auth import HTTPBasicAuth

# Configuración de la conexión a F5

f5_host = 'https://52.176.220.110:8443/mgmt/shared/appsvcs/declare'  # Reemplaza <F5_HOST> con la dirección IP o el nombre de host de tu F5
username = 'admin'  # Cambia a tus credenciales de F5
password = 'f5DEMOs4uLATAM'  # Cambia a tus credenciales de F5

# Definición del Virtual Server usando AS3
as3_declaration = {
    "$schema": "https://raw.githubusercontent.com/F5Networks/f5-appsvcs-extension/master/schema/latest/as3-schema-3.10.0-5.json",
    "class": "AS3",
    "action": "deploy",
    "persist": True,
    "declaration": {
        "class": "ADC",
        "schemaVersion": "3.10.0",
        "id": "lmnop12345",
        "label": "GoSmarter",
        "remark": "An HTTP and an HTTPS application",
        "controls": {
            "trace": True
        },
        "Produccion_01": {
            "class": "Tenant"
        }
    }
}

# Headers para la solicitud
headers = {
    'Content-Type': 'application/json',
    'X-F5-Auth-Token': '2WHNQVMRRBEFIZDOIUWJUIZ2Y4',
    #'Authorization': 'Basic ' + requests.auth._basic_auth_str(username, password)
}

# Realizar la solicitud POST a la API de AS3
response = requests.post(f5_host, headers=headers, data=json.dumps(as3_declaration), verify=False)

# Manejar la respuesta
if response.status_code == 200:
    print("Declaración AS3 enviada con éxito.")
    print("Respuesta del servidor F5:")
    print(json.dumps(response.json(), indent=4))
else:
    print(f"Error al enviar la declaración AS3: {response.status_code}")
    print(response.text)
