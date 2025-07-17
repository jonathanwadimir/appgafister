import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from web.utils.auth import login, get_current_user

def render_login():
    st.title("🔐 Iniciar Sesión")
    username = st.text_input("RUT (usuario)", placeholder="Ej: 12345678-9")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        token = login(username, password)
        if token:
            user = get_current_user(token)
            if user:
                st.session_state.token = token
                st.session_state.user = user
                st.success(f"✅ Bienvenido {user.get('nombre', user.get('rut'))}")
                st.rerun()  # ✅ Reemplazo moderno de experimental_rerun
            else:
                st.error("❌ Error al obtener los datos del usuario.")
        else:
            st.error("❌ Usuario o contraseña incorrectos.")
