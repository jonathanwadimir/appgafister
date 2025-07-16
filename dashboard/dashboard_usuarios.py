import streamlit as st
import httpx

st.title("🔐 Registro de Usuarios (Admin, Técnico, Cliente)")

# === Formulario de creación de usuario ===
with st.form("crear_usuario_form"):
    st.subheader("📝 Crear Nuevo Usuario")
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    rol = st.selectbox("Rol", ["admin", "tecnico", "cliente"])

    submitted = st.form_submit_button("Registrar Usuario")

    if submitted:
        if not username or not password:
            st.warning("Debe completar todos los campos.")
        else:
            payload = {
                "username": username,
                "password": password,
                "rol": rol
            }

            try:
                response = httpx.post("http://localhost:8000/auth/registro", json=payload)
                if response.status_code == 200:
                    st.success(f"✅ Usuario '{username}' creado con rol '{rol}'")
                elif response.status_code == 400:
                    st.error("❌ El usuario ya existe.")
                else:
                    st.error(f"⚠️ Error inesperado: {response.text}")
            except Exception as e:
                st.error(f"⚠️ No se pudo conectar al backend: {e}")
