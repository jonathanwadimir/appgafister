import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="APPGafister Dashboard", page_icon="🛠️")

if "token" not in st.session_state:
    st.session_state.token = ""

st.title("🛠️ APPGafister Dashboard")

# Login
st.subheader("Iniciar Sesión")
username = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

if st.button("Ingresar"):
    response = requests.post(f"{API_URL}/auth/login", data={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        st.session_state.token = token
        st.success(f"✅ Bienvenido {username}")
    else:
        st.error("❌ Usuario o contraseña incorrectos")

# Mensaje de advertencia
if st.session_state.token:
    st.info(
        "⚠️ <b>Advertencia:</b> El acceso a este sistema está reservado a personal autorizado. "
        "Toda actividad es monitoreada.",
        unsafe_allow_html=True
    )
