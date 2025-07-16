import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# === LOGIN ===
def login():
    st.title("🔐 Login")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        data = {"username": username, "password": password}
        try:
            r = requests.post(f"{API_URL}/auth/login", data=data)
            if r.status_code == 200:
                token = r.json().get("access_token")
                if token:
                    st.session_state["token"] = token
                    user = requests.get(f"{API_URL}/auth/users/me", headers={"Authorization": f"Bearer {token}"}).json()
                    st.session_state["usuario_actual"] = user
                    st.success(f"✅ Login exitoso como {user['username']} ({user['rol']})")
                    st.rerun()
                else:
                    st.error("❌ Token no recibido")
            else:
                st.error("❌ Usuario o contraseña incorrectos")
        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")

# === HEADER CON TOKEN ===
def get_headers():
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

# === TICKETS ===
def listar_tickets():
    st.subheader("📋 Tickets registrados")
    try:
        r = requests.get(f"{API_URL}/tickets/", headers=get_headers())
        if r.status_code == 200:
            tickets = r.json()
            if not tickets:
                st.info("No hay tickets registrados.")
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
            st.error("Error al cargar tickets")
    except Exception as e:
        st.error(f"Error: {e}")

# === CREAR TICKET (admin) ===
def crear_ticket():
    if st.session_state.get("usuario_actual", {}).get("rol") != "admin":
        st.warning("🔒 Solo los administradores pueden crear tickets.")
        return
    st.subheader("🆕 Crear nuevo Ticket")
    cliente_id = st.number_input("ID Cliente", min_value=1, step=1)
    descripcion = st.text_area("Descripción del problema")
    if st.button("Crear Ticket"):
        data = {
            "cliente_id": cliente_id,
            "descripcion": descripcion
        }
        r = requests.post(f"{API_URL}/ticket/", json=data, headers=get_headers())
        if r.status_code in [200, 201]:
            st.success("✅ Ticket creado correctamente")
            st.rerun()
        else:
            st.error(f"❌ Error al crear ticket: {r.text}")

# === ASIGNAR TÉCNICO (admin) ===
def asignar_tecnico():
    if st.session_state.get("usuario_actual", {}).get("rol") != "admin":
        st.warning("🔒 Solo los administradores pueden asignar técnicos.")
        return
    st.subheader("👷 Asignar Técnico a Ticket")
    ticket_id = st.number_input("ID del Ticket", min_value=1, step=1, key="ticket_id")
    tecnico_id = st.number_input("ID del Técnico", min_value=1, step=1, key="tecnico_id")
    if st.button("Asignar Técnico"):
        data = {"tecnico_id": tecnico_id}
        r = requests.put(f"{API_URL}/ticket/{ticket_id}/asignacion", json=data, headers=get_headers())
        if r.status_code == 200:
            st.success("✅ Técnico asignado correctamente")
            st.rerun()
        else:
            st.error(f"❌ Error al asignar técnico: {r.text}")

# === REGISTRAR USUARIO (admin) ===
def registrar_usuario():
    if st.session_state.get("usuario_actual", {}).get("rol") != "admin":
        st.warning("🔒 Solo los administradores pueden registrar usuarios.")
        return
    st.subheader("👤 Registrar nuevo Usuario")
    username = st.text_input("Nombre de usuario", key="reg_username")
    password = st.text_input("Contraseña", type="password", key="reg_password")
    rol = st.selectbox("Rol", ["cliente", "tecnico", "admin"], key="reg_rol")
    if st.button("Registrar Usuario"):
        data = {
            "username": username,
            "password": password,
            "rol": rol
        }
        try:
            r = requests.post(f"{API_URL}/auth/registro", json=data, headers=get_headers())
            if r.status_code in [200, 201]:
                st.success("✅ Usuario registrado correctamente")
                st.rerun()
            else:
                st.error(f"❌ Error: {r.text}")
        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")

# === GESTIONAR USUARIOS (admin) ===
def gestionar_usuarios():
    if st.session_state.get("usuario_actual", {}).get("rol") != "admin":
        st.warning("🔒 Solo los administradores pueden gestionar usuarios.")
        return
    st.subheader("👥 Gestionar Usuarios")
    try:
        r = requests.get(f"{API_URL}/usuarios/", headers=get_headers())
        if r.status_code == 200:
            usuarios = r.json()
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
                        res = requests.put(f"{API_URL}/usuarios/{usuario['id']}", json=data, headers=get_headers())
                        if res.status_code == 200:
                            st.success(f"Rol de {usuario['username']} actualizado a {nuevo_rol}")
                            st.rerun()
                        else:
                            st.error(f"Error actualizando rol: {res.text}")
                if st.button(f"Eliminar usuario", key=f"del_{usuario['id']}"):
                    if st.checkbox(f"Confirmar eliminación de {usuario['username']}", key=f"conf_{usuario['id']}"):
                        res = requests.delete(f"{API_URL}/usuarios/{usuario['id']}", headers=get_headers())
                        if res.status_code == 204:
                            st.success(f"Usuario {usuario['username']} eliminado")
                            st.rerun()
                        else:
                            st.error(f"Error eliminando usuario: {res.text}")
                st.markdown("---")
        else:
            st.error("Error al cargar usuarios")
    except Exception as e:
        st.error(f"Error: {e}")

# === POSTULAR A TICKETS (solo técnico) ===
def postular_a_tickets():
    if st.session_state.get("usuario_actual", {}).get("rol") != "tecnico":
        return
    st.subheader("🛠️ Tickets disponibles para postular")
    try:
        r = requests.get(f"{API_URL}/tickets/", headers=get_headers())
        if r.status_code == 200:
            tickets = [t for t in r.json() if t["estado_asignacion"] == "pendiente"]
            if not tickets:
                st.info("No hay tickets disponibles.")
                return
            for t in tickets:
                with st.expander(f"🔧 Ticket #{t['id']} — Cliente {t['cliente_id']}"):
                    st.write(f"📄 Descripción: {t['descripcion']}")
                    if st.button("✅ Postularme", key=f"post_{t['id']}"):
                        tecnico_id = st.session_state["usuario_actual"]["id"]
                        data = {
                            "ticket_id": t["id"],
                            "tecnico_id": tecnico_id
                        }
                        resp = requests.post(f"{API_URL}/postulaciones/", json=data, headers=get_headers())
                        if resp.status_code in [200, 201]:
                            st.success("✅ Postulación enviada correctamente")
                            st.rerun()
                        else:
                            st.error(f"❌ Error al postular: {resp.text}")
        else:
            st.error("Error al cargar tickets.")
    except Exception as e:
        st.error(f"Error: {e}")

# === EVALUAR SERVICIO ===
def evaluar_ticket():
    st.subheader("🌟 Evaluar Servicio Técnico")
    ticket_id = st.number_input("ID del Ticket a evaluar", min_value=1, step=1)
    puntuacion = st.slider("Puntaje (1 = Malo, 5 = Excelente)", 1, 5, 3)
    comentario = st.text_area("Comentario adicional (opcional)")
    if st.button("Enviar Evaluación"):
        data = {
            "ticket_id": ticket_id,
            "puntuacion": puntuacion,
            "comentario": comentario
        }
        try:
            r = requests.post(f"{API_URL}/evaluaciones/", json=data, headers=get_headers())
            if r.status_code in [200, 201]:
                st.success("✅ Evaluación enviada correctamente")
                st.rerun()
            else:
                st.error(f"❌ Error al enviar evaluación: {r.text}")
        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")

# === DASHBOARD ===
def dashboard():
    st.sidebar.success("Sesión activa")
    if st.sidebar.button("🔓 Cerrar sesión"):
        st.session_state.pop("token", None)
        st.session_state.pop("usuario_actual", None)
        st.rerun()

    user = st.session_state.get("usuario_actual", {})
    rol = user.get("rol", "desconocido")
    st.title(f"🛠️ Dashboard - Rol: {rol.capitalize()}")

    if rol == "admin":
        menu = st.sidebar.radio("Menú", ["Tickets", "Registrar Usuario", "Gestionar Usuarios", "Evaluar Servicio"])
    elif rol == "tecnico":
        menu = st.sidebar.radio("Menú", ["Tickets", "Postular a Tickets", "Evaluar Servicio"])
    elif rol == "cliente":
        menu = st.sidebar.radio("Menú", ["Tickets", "Evaluar Servicio"])
    else:
        st.error("❌ Rol no reconocido.")
        return

    if menu == "Tickets":
        listar_tickets()
        if rol == "admin":
            st.markdown("---")
            crear_ticket()
            st.markdown("---")
            asignar_tecnico()
    elif menu == "Registrar Usuario":
        registrar_usuario()
    elif menu == "Gestionar Usuarios":
        gestionar_usuarios()
    elif menu == "Postular a Tickets":
        postular_a_tickets()
    elif menu == "Evaluar Servicio":
        evaluar_ticket()

# === MAIN ===
def main():
    if "token" not in st.session_state:
        login()
    else:
        dashboard()

if __name__ == "__main__":
    main()
