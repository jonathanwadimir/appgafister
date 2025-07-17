import streamlit as st
import requests
from web.config import API_URL

def render(token: str):
    st.subheader("📋 Lista de Tickets")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/tickets/", headers=headers)
        if response.status_code == 200:
            tickets = response.json()
            if tickets:
                for t in tickets:
                    st.markdown(f"""
                    ---
                    🔧 Ticket #{t['id']}
                    - 📝 Descripción: {t['descripcion']}
                    - 👤 Cliente ID: {t['cliente_id']}
                    - 🧑‍🔧 Técnico ID: {t.get('tecnico_id') or 'No asignado'}
                    - 🏁 Estado: `{t['estado_asignacion']}`
                    """)
            else:
                st.info("No hay tickets registrados.")
        else:
            st.error(f"Error: {response.text}")
    except Exception as e:
        st.error(f"Error al obtener tickets: {e}")
