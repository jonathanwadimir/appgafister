import streamlit as st
import requests
from web.config import API_URL

def render(token: str):
    st.subheader("👷 Lista de Técnicos")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/tecnicos", headers=headers)
        if response.status_code == 200:
            tecnicos = response.json()
            if tecnicos:
                st.table(tecnicos)
            else:
                st.info("No hay técnicos registrados.")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error al obtener técnicos: {e}")
