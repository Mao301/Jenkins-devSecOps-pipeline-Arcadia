import requests
import json
import os
import urllib3
from requests.auth import HTTPBasicAuth


# Deshabilitar advertencias de certificados SSL autofirmados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración de la conexión a F5

f5_host = 'https://52.176.220.110:8443/mgmt/shared/appsvcs/declare'  # Reemplaza <F5_HOST> con la dirección IP o el nombre de host de tu F5
#username = ''  # Cambia a tus credenciales de F5
#password = ''  # Cambia a tus credenciales de F5
username = os.getenv('F5_USERNAME') # Se toma como variable de entorno del pipeline de CI/CD
password = os.getenv('F5_PASSWORD') # Se toma como variable de entorno del pipeline de CI/CD

auth_token = os.getenv('AUTH_TOKEN') # Toma el token de autorización como variable de entorno

# Cargar el template de AS3 desde el repositorio
with open('AS3_Template_Create_APP.json', 'r') as template_file:
    as3_template = template_file.read()

# Cargar los parámetros desde el archivo
with open('AS3_Params_For_CreateAPP.json', 'r') as params_file:
    params = json.load(params_file)

# Realizar la sustitución de variables en el template
as3_declaration = as3_template
for key, value in params.items():
    as3_declaration = as3_declaration.replace('${' + key + '}', str(value))

# Convertir la declaración a un diccionario Python
as3_declaration = json.loads(as3_declaration)


# Headers para la solicitud
headers = {
    'Content-Type': 'application/json',
    'X-F5-Auth-Token': auth_token
    #'Authorization': 'Basic ' + requests.auth._basic_auth_str(username, password)
}

# Realizar la solicitud POST a la API de AS3
response = requests.post(f5_host, headers=headers, data=json.dumps(as3_declaration), verify=False)

# Manejar la respuesta
if response.status_code == 200:
    print("Declaración AS3 enviada con éxito para la creación.")
    print("Respuesta del servidor F5:")
    print(json.dumps(response.json(), indent=4))
else:
    print(f"Error al enviar la declaración AS3: {response.status_code}")
    print(response.headers)
    print(response.text)
    
