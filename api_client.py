import requests
API_URL = "https://jsonplaceholder.typicode.com/users"

def obtener_usuarios_api():
    response = requests.get(API_URL, timeout=10)
    
    if response.status_code==200:
        return response.json()
    
    else:
        return[]
    
        
