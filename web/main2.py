import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from web.utils.auth import login, get_current_user
from web.views import (
    home,
    tecnicos,
    tickets,
    postulaciones,
    evaluaciones,
    clientes,
    usuarios
)

st.set_page_config(page_title="APPGafister Dashboard", page_icon="🛠️")

if "token" not in st.session_state:
    st.session_state.token = ""
if "user" not in st.session_state:
    st.session_state.user = None

st.title("🛠️ APPGafister Dashboard")

if not st.session_state.token:
    st.subheader("Iniciar Sesión")
    username = st.text_input("RUT (usuario)", placeholder="Ej: 12345678-9")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        token = login(username, password)
        if token:
            user = get_current_user(token)
            if user:
                st.session_state.token = token
                st.session_state.user = user
                st.success(f"✅ Bienvenido {user.get('nombre', user.get('username', 'Usuario'))}")
                st.experimental_rerun()
            else:
                st.error("Error al obtener datos de usuario.")
        else:
            st.error("❌ Usuario o contraseña incorrectos")
else:
    user = st.session_state.user
    token = st.session_state.token

    menu = ["Inicio", "Técnicos", "Tickets", "Postulaciones", "Evaluaciones", "Clientes"]
    if user.get("rol") == "admin":
        menu.append("Usuarios")
    menu.append("Cerrar Sesión")

    choice = st.sidebar.selectbox("Menú", menu)

    if choice == "Inicio":
        home.render(user)
    elif choice == "Técnicos":
        tecnicos.render(token)
    elif choice == "Tickets":
        tickets.render(token)
    elif choice == "Postulaciones":
        postulaciones.render(token)
    elif choice == "Evaluaciones":
        evaluaciones.render(token)
    elif choice == "Clientes":
        clientes.render(token)
    elif choice == "Usuarios" and user.get("rol") == "admin":
        usuarios.render(token)
    elif choice == "Cerrar Sesión":
        st.session_state.token = ""
        st.session_state.user = None
        st.experimental_rerun()
