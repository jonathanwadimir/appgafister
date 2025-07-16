import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # Cambia según tu backend

def login(username, password):
    response = requests.post(f"{API_URL}/login", data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def get_user_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/users/me", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def main():
    st.title("Dashboard APPGafister")

    if "token" not in st.session_state:
        st.session_state.token = None

    if st.session_state.token is None:
        st.subheader("Login")
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            token = login(username, password)
            if token:
                st.session_state.token = token
                st.success("Login exitoso!")
            else:
                st.error("Usuario o contraseña incorrectos")
    else:
        user_info = get_user_info(st.session_state.token)
        if user_info:
            st.write(f"Bienvenido, **{user_info['username']}** (Rol: {user_info['rol']})")
            # Aquí puedes agregar más funcionalidades para el dashboard
            st.button("Cerrar sesión", on_click=lambda: st.session_state.clear())
        else:
            st.error("Token inválido o expirado")
            st.session_state.token = None

if __name__ == "__main__":
    main()
