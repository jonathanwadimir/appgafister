from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas import UserCreate, Token, UserOut
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

router = APIRouter()

# Seguridad
SECRET_KEY = "tu_secreto_super_seguro_123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hashear_password(password):
    return pwd_context.hash(password)

def crear_token_acceso(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(Usuario).filter(Usuario.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

@router.post("/registro", status_code=status.HTTP_201_CREATED)
async def registrar(usuario: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).filter(Usuario.username == usuario.username))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Usuario ya registrado")

    hashed_pwd = hashear_password(usuario.password)
    nuevo_usuario = Usuario(
        username=usuario.username,
        hashed_password=hashed_pwd,
        rol=usuario.rol
    )
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return {"message": f"Usuario '{usuario.username}' registrado correctamente con rol '{usuario.rol}'"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).filter(Usuario.username == form_data.username))
    usuario_db = result.scalar_one_or_none()
    if not usuario_db or not verificar_password(form_data.password, usuario_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    token = crear_token_acceso({"sub": usuario_db.username, "rol": usuario_db.rol})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserOut)
async def leer_usuario_actual(current_user: Usuario = Depends(get_current_user)):
    return current_user
