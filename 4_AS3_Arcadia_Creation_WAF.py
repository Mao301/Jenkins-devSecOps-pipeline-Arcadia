import requests
import json
import os
from requests.auth import HTTPBasicAuth

# Configuración de la conexión a F5

f5_host = 'https://52.176.220.110:8443/mgmt/shared/appsvcs/declare'  # Reemplaza <F5_HOST> con la dirección IP o el nombre de host de tu F5
#username = ''  # Cambia a tus credenciales de F5
#password = ''  # Cambia a tus credenciales de F5
username = os.getenv('F5_USERNAME') # Se toma como variable de entorno del pipeline de CI/CD
password = os.getenv('F5_PASSWORD') # Se toma como variable de entorno del pipeline de CI/CD

auth_token = os.getenv('AUTH_TOKEN') # Toma el token de autorización como variable de entorno
# Definición del Virtual Server usando AS3
as3_declaration = {
    "class": "AS3",
    "declaration": {
        "class": "ADC",
        "schemaVersion": "3.26.0",
        "id": "example-declaration",
        "label": "Evertec",
        "remark": "Generic HTTP applications",
        "Produccion_01": {
            "class": "Tenant",
            "vs_Application_http_80": {
                "class": "Application",
                "template": "generic",
                "vs_arcadia_http_80": {
                    "class": "Service_HTTP",
                    "virtualAddresses": [
                        "10.1.10.4"  # Cambia esta dirección IP al Virtual IP de tu F5
                    ],
                    "pool": "pool_arcadia",
                    "virtualPort": 80,
                    "securityLogProfiles": [
                    	{
                    		"bigip": "/Common/Log all requests"
                    	}
                    ],
                    "policyWAF": {
                    	"use": "ArcadiaWAF"
                    },
                },
                "pool_arcadia": {
                    "class": "Pool",
                    "monitors": [
                        "http"
                    ],
                    "members": [
                        {
                            "servicePort": 80,
                            "serverAddresses": [
                                "10.1.10.5"  # Cambia esta dirección IP a la de tu servidor backend
                            ]
                        }
                    ]
                },
                "ArcadiaWAF": {
                    "class": "WAF_Policy",
                    "url": "https://raw.githubusercontent.com/cavalen/acme/master/declarative-waf.json",
                    "ignoreChanges": True
                }
            }
        }
    }
}

# Headers para la solicitud
headers = {
    'Content-Type': 'application/json',
    'X-F5-Auth-Token': auth_token
    #'X-F5-Auth-Token': '',
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
