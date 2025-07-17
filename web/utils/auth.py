import requests
from web.config import API_URL

def login(username: str, password: str) -> str | None:
    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(f"{API_URL}/auth/login", data=data, headers=headers)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"[login] Falló login. Status: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[login] Error de conexión: {e}")
    return None

def get_current_user(token: str) -> dict | None:
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/users/me", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[get_current_user] Falló. Status: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[get_current_user] Error de conexión: {e}")
    return None
