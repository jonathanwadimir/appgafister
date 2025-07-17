import streamlit as st
import requests
from web.config import API_URL

def render(token: str):
    st.subheader("👥 Lista de Clientes")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/clientes", headers=headers)
        if response.status_code == 200:
            clientes = response.json()
            if clientes:
                st.table(clientes)
            else:
                st.info("No hay clientes registrados.")
        else:
            st.error(f"Error: {response.text}")
    except Exception as e:
        st.error(f"Error al obtener clientes: {e}")
