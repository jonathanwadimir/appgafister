import streamlit as st
import requests
from dashboard.utils import API_URL, get_headers

def login():
    st.title("🔐 Login")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        data = {"username": username, "password": password}
        try:
            r = requests.post(f"{API_URL}/auth/login", data=data)
            if r.status_code == 200:
                token = r.json().get("access_token")
                st.session_state["token"] = token
                st.success("✅ Login exitoso")
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")

def get_current_user():
    try:
        r = requests.get(f"{API_URL}/users/me", headers=get_headers())
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None
