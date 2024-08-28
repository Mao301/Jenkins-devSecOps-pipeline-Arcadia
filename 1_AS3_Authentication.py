import requests
import json
import os
from requests.auth import HTTPBasicAuth


# Configuración de la conexión a F5

f5_host = 'https://52.176.220.110:8443//mgmt/shared/authn/login'  # Reemplaza <F5_HOST> con la dirección IP o el nombre de host de tu F5
#username = 'admin'  # Cambia a tus credenciales de F5
#password = 'f5DEMOs4uLATAM'  # Cambia a tus credenciales de F5

username = os.getenv('F5_USERNAME')
password = os.getenv('F5_PASSWORD')

# Definición del Virtual Server usando AS3
as3_declaration = {
    "username":"",
    #"username":"admin",
    "password":"",
    #"password":"f5DEMOs4uLATAM",
    "loginProviderName":"tmos"
}

# Reemplazar valores en la declaración AS3
as3_declaration["username"] = username
as3_declaration["password"] = password

# Headers para la solicitud
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + requests.auth._basic_auth_str(username, password)
}

# Realizar la solicitud POST a la API de AS3
response = requests.post(f5_host, headers=headers, data=json.dumps(as3_declaration), verify=False)
response_data = response.json()
#token = response_data.get('token.token') 
token = response_data.get('token', {}).get('token')
# Manejar la respuesta
if response.status_code == 200:
    print("Declaración AS3 enviada con éxito para autenticacion.")
    print("Respuesta del servidor F5_:")
    #if token: print(f"##vso[task.setvariable variable=AUTH_TOKEN; issecret=true]{token}")
    if token: print(f"AUTH_TOKEN={token}")
    #print(f"Authentication Token: {token}")
    #print(json.dumps(response.json(), indent=4))
else:
    print(f"Error al enviar la declaración AS3 2: {response.status_code}")
    print(response.headers)
    print(response.text)
    
