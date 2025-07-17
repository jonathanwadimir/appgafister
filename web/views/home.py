import streamlit as st

def render(user: dict):
    st.header(f"👋 Bienvenido, {user.get('nombre', user.get('username', 'Usuario'))}")
    st.markdown(f"📌 Rol: **{user.get('rol', 'desconocido').capitalize()}**")

    st.markdown(
        """
        ⚠️ <b>Advertencia:</b> El acceso a este sistema está reservado a personal autorizado.  
        Toda actividad es monitoreada.
        """,
        unsafe_allow_html=True
    )
