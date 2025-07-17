import streamlit as st
import requests
from web.config import API_URL

def render(token: str):
    st.subheader("🌟 Lista de Evaluaciones")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/evaluaciones", headers=headers)
        if response.status_code == 200:
            evaluaciones = response.json()
            if evaluaciones:
                st.table(evaluaciones)
            else:
                st.info("No hay evaluaciones registradas.")
        else:
            st.error(f"Error: {response.text}")
    except Exception as e:
        st.error(f"Error al obtener evaluaciones: {e}")
