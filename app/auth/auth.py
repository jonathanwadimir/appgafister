from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud.usuario import get_user_by_username, verify_password, create_user
from app.schemas.usuario import UserOut, UserCreate, Token
from app.models.usuario import Usuario

SECRET_KEY = "tu_secreto_super_seguro_123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

# === Autenticación ===
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

# === Crear Token JWT ===
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# === Registro de Usuario ===
@router.post("/registro", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    created_user = await create_user(db, user.username, user.password, user.rol)
    return created_user

# === Login ===
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username, "rol": user.rol})
    return {"access_token": access_token, "token_type": "bearer"}

# === Obtener usuario actual desde JWT ===
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        rol: str | None = payload.get("rol")
        if username is None or rol is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_username(db, username=username)
    if user is None or user.rol != rol:
        raise credentials_exception
    return user

# === Requiere un rol específico ===
def require_role(role: str):
    async def role_checker(current_user: Usuario = Depends(get_current_user)):
        if current_user.rol != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permisos suficientes. Se requiere rol '{role}'.",
            )
        return current_user
    return role_checker

# === Obtener usuario autenticado ===
@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: Usuario = Depends(get_current_user)):
    return current_user
