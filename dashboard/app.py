import streamlit as st
import requests

# 👉 URL del backend FastAPI
API_URL = "http://localhost:8000"

# Configuración de la página
st.set_page_config(page_title="APPGafister Dashboard", page_icon="🛠️", layout="centered")

# Inicializar session_state
if "token" not in st.session_state:
    st.session_state.token = None
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# ------------------------------------------
# 👉 Función para autenticarse
# ------------------------------------------
def login(username, password):
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.session_state.usuario = username
            return True
        else:
            return False
    except Exception as e:
        st.error("Error de conexión con el servidor.")
        return False

# ------------------------------------------
# 👉 Interfaz de Login
# ------------------------------------------
def mostrar_login():
    st.title("🛠️ APPGafister Dashboard")
    st.subheader("Iniciar Sesión")

    username = st.text_input("Usuario", key="username_input")
    password = st.text_input("Contraseña", type="password", key="password_input")

    if st.button("Iniciar Sesión"):
        if login(username, password):
            st.success(f"✅ Bienvenido {username}")
            st.warning("⚠️ Advertencia: El acceso a este sistema está reservado a personal autorizado.")
        else:
            st.error("❌ Usuario o contraseña incorrectos")

# ------------------------------------------
# 👉 Interfaz del Dashboard
# ------------------------------------------
def mostrar_dashboard():
    st.title(f"🎛️ Panel de control - {st.session_state.usuario}")

    st.success("Sesión iniciada correctamente.")

    st.markdown("---")
    st.subheader("🔍 Opciones del sistema")
    st.write("Aquí puedes integrar funcionalidades como:")
    st.markdown("- Visualizar técnicos")
    st.markdown("- Visualizar tickets")
    st.markdown("- Crear usuarios")
    st.markdown("- ...")

    # Botón de cerrar sesión
    if st.button("🔓 Cerrar Sesión"):
        st.session_state.token = None
        st.session_state.usuario = None
        st.experimental_rerun()  # Reiniciar la app para volver al login

# ------------------------------------------
# 👉 Lógica principal
# ------------------------------------------
if st.session_state.token is None:
    mostrar_login()
else:
    mostrar_dashboard()
