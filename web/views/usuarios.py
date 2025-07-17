import streamlit as st
import requests
from web.config import API_URL

def render(token: str):
    st.subheader("👤 Gestión de Usuarios (Admin)")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/usuarios", headers=headers)
        if response.status_code == 200:
            usuarios = response.json()
            if not usuarios:
                st.info("No hay usuarios registrados.")
                return

            for usuario in usuarios:
                st.markdown(f"**ID:** {usuario['id']} — **Usuario:** {usuario['username']} — **Rol:** {usuario['rol']}")

                cols = st.columns([1, 3, 1])
                with cols[1]:
                    nuevo_rol = st.selectbox(
                        "Cambiar rol",
                        ["cliente", "tecnico", "admin"],
                        index=["cliente", "tecnico", "admin"].index(usuario['rol']),
                        key=f"rol_{usuario['id']}"
                    )
                with cols[2]:
                    if st.button("Actualizar rol", key=f"act_{usuario['id']}"):
                        data = {"rol": nuevo_rol}
                        res = requests.put(f"{API_URL}/usuarios/{usuario['id']}", json=data, headers=headers)
                        if res.status_code == 200:
                            st.success(f"Rol de {usuario['username']} actualizado a {nuevo_rol}")
                            st.experimental_rerun()
                        else:
                            st.error(f"Error actualizando rol: {res.text}")

                if st.button(f"Eliminar usuario", key=f"del_{usuario['id']}"):
                    if st.checkbox(f"Confirmar eliminación de {usuario['username']}", key=f"conf_{usuario['id']}"):
                        res = requests.delete(f"{API_URL}/usuarios/{usuario['id']}", headers=headers)
                        if res.status_code == 204:
                            st.success(f"Usuario {usuario['username']} eliminado")
                            st.experimental_rerun()
                        else:
                            st.error(f"Error eliminando usuario: {res.text}")

                st.markdown("---")
        else:
            st.error(f"Error al cargar usuarios: {response.text}")
    except Exception as e:
        st.error(f"Error al obtener usuarios: {e}")
