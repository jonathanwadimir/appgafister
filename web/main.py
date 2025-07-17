import streamlit as st
from web.utils.auth import login, get_current_user
from web.views import (
    home,
    tecnicos,
    tickets,
    postulaciones,
    evaluaciones,
    clientes,
    usuarios
)
from web.utils.session import logout, is_authenticated

st.set_page_config(page_title="APPGafister Dashboard", page_icon="🛠️")

# Inicializar estado de sesión si no existe
if "token" not in st.session_state:
    st.session_state.token = ""
if "user" not in st.session_state:
    st.session_state.user = None

# Si no hay sesión activa, mostrar login
if not is_authenticated():
    from web.pages import login as login_page
    login_page.render_login()
else:
    user = st.session_state.user
    token = st.session_state.token

    st.title("🛠️ APPGafister Dashboard")
    st.sidebar.markdown(f"👤 **{user.get('nombre', user.get('rut', 'Usuario'))}** ({user.get('rol')})")

    # Menú de navegación lateral
    menu = ["Inicio", "Técnicos", "Tickets", "Postulaciones", "Evaluaciones", "Clientes"]
    if user.get("rol") == "admin":
        menu.append("Usuarios")
    menu.append("Cerrar Sesión")

    choice = st.sidebar.selectbox("Menú", menu)

    # Rutas según elección del usuario
    if choice == "Inicio":
        home.render(user)
    elif choice == "Técnicos":
        tecnicos.render(token)
    elif choice == "Tickets":
        tickets.render(token)
    elif choice == "Postulaciones":
        postulaciones.render(token)
    elif choice == "Evaluaciones":
        evaluaciones.render(token)
    elif choice == "Clientes":
        clientes.render(token)
    elif choice == "Usuarios" and user.get("rol") == "admin":
        usuarios.render(token)
    elif choice == "Cerrar Sesión":
        logout()
