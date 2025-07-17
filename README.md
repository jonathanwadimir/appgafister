# 🚰 APPGafister

**APPGafister** es una plataforma completa para la gestión de tickets técnicos en servicios de gasfitería. Permite registrar técnicos, clientes, asignar tickets, realizar postulaciones, evaluar servicios y más. Está desarrollada con **FastAPI**, **SQLAlchemy (async)**, **Streamlit** y **Telegram Bot**.

---

## 🌐 Características principales

- **📋 Gestión de tickets**: creación, asignación automática, evaluación por clientes.
- **👷 Postulación de técnicos**: técnicos pueden postularse a tickets abiertos.
- **⚙️ Asignación automática**: selección inteligente del mejor técnico disponible.
- **📊 Dashboard administrativo** con **Streamlit**.
- **💬 Integración con Bot de Telegram** (postulaciones y notificaciones).
- **🔐 Autenticación con JWT** y control por roles (admin, técnico, cliente).
- **📱 Preparado para conexión con apps móviles Android.**

---

## 🛠️ Tecnologías utilizadas

| Tecnología      | Descripción                           |
|----------------|----------------------------------------|
| FastAPI        | Backend REST API                       |
| SQLAlchemy     | ORM asincrónico con `aiosqlite`        |
| Streamlit      | Dashboard web interactivo              |
| Telegram Bot   | Interacción de técnicos vía Telegram   |
| JWT            | Autenticación segura                   |
| SQLite         | Base de datos liviana para desarrollo  |

---

## 🚀 Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/jonathanwadimir/appgafister.git
cd appgafister
2. Crea entorno virtual e instala dependencias
bash
Copiar
Editar
python -m venv venv
venv\Scripts\activate   # En Windows
pip install -r requirements.txt
3. Ejecuta la API con FastAPI
bash
Copiar
Editar
uvicorn app.main:app --reload
Abre tu navegador en: http://127.0.0.1:8000/docs

4. Ejecuta el dashboard Streamlit
bash
Copiar
Editar
streamlit run dashboard/app.py
🧪 Usuario administrador por defecto
Se crea automáticamente al iniciar la app:

Usuario (RUT): admin1

Contraseña: admin123

Rol: admin

Puedes cambiar estos valores en app/utils/create_admin.py.

📌 Estructura del proyecto
bash
Copiar
Editar
appgafister/
├── app/
│   ├── models/           # Modelos SQLAlchemy
│   ├── schemas/          # Esquemas Pydantic
│   ├── crud/             # Lógica de base de datos
│   ├── routers/          # Rutas FastAPI
│   ├── auth/             # Autenticación JWT
│   └── main.py           # Punto de entrada FastAPI
│
├── dashboard/            # App de Streamlit
│   └── app.py
├── requirements.txt
└── README.md
📦 Requisitos
Python 3.10+

Git

Streamlit

Cuenta de Telegram para usar el bot (opcional)

🤝 Contribuciones
¡Contribuciones son bienvenidas! Puedes abrir issues o enviar pull requests para mejorar funcionalidades.

📜 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

📫 Autor
Jonathan Wladimir
🔗 github.com/jonathanwadimir

yaml
Copiar
Editar

---

### ✅ requerimiento

📌 Instrucciones
Guarda este contenido como requirements.txt en la raíz del proyecto (appgafister/).

Instala las dependencias con:

bash
Copiar
Editar
pip install -r requirements.txt