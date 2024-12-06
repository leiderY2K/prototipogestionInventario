import os
import webbrowser
import msal
from dotenv import load_dotenv

client_id = '3f6393f5-c965-4c3c-8cc2-e1e94ec218b1'

MS_GRAPH_BASE_URL = 'http://graph.microsoft.com/v1.0'

def get_access_token(scopes):
    # Inicializar el cliente
    client = msal.PublicClientApplication(
        client_id=client_id,
        authority="https://login.microsoftonline.com/common/"
    )
    try:
        # Iniciar el flujo de autenticación de dispositivo
        flow = client.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            print(f"Error: {flow.get('error')}")
            print(f"Descripción del error: {flow.get('error_description')}")
            return None

        print(f"Código de usuario: {flow['user_code']}")
        print(f"Por favor, ve a {flow['verification_uri']} e ingresa el código.")
        print("Flujo completo:", flow)
        
        # Abrir el navegador web
        webbrowser.open(flow['verification_uri'])
        
        # Adquirir el token
        token_response = client.acquire_token_by_device_flow(flow)
        
        if "access_token" in token_response:
            print("Autenticación exitosa!")
            print(f"Token de acceso: {token_response['access_token'][:10]}...") # Mostrar solo los primeros 10 caracteres
            return token_response['access_token']
        else:
            print(f"Error en la autenticación: {token_response.get('error')}")
            print(f"Descripción del error: {token_response.get('error_description')}")
            return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")
        return None

def main():
    # Cargar variables de entorno
    load_dotenv()
    
    SCOPES = ['User.Read', 'Files.Read.All', 'Files.Read']
    access_token = get_access_token(SCOPES)
    
    if access_token:
        print("Token obtenido exitosamente. Puedes usarlo para hacer solicitudes a Microsoft Graph.")
    else:
        print("No se pudo obtener el token de acceso.")

if __name__ == "__main__":
    main()