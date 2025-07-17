import streamlit as st

def logout():
    st.session_state.token = ""
    st.session_state.user = None
    st.success("Sesión cerrada.")
    st.rerun()  # ✅ Reemplazo moderno de experimental_rerun

def is_authenticated():
    return bool(st.session_state.get("token") and st.session_state.get("user"))
