import streamlit as st
import requests
from web.config import API_URL

def render(token: str):
    st.subheader("📝 Lista de Postulaciones")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/postulaciones", headers=headers)
        if response.status_code == 200:
            postulaciones = response.json()
            if postulaciones:
                st.table(postulaciones)
            else:
                st.info("No hay postulaciones registradas.")
        else:
            st.error(f"Error: {response.text}")
    except Exception as e:
        st.error(f"Error al obtener postulaciones: {e}")
