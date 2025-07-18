from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import TokenData

SECRET_KEY = "tu_clave_secreta_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        rut: str = payload.get("sub")
        if rut is None:
            raise credentials_exception
        token_data = TokenData(rut=rut)
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(Usuario).where(Usuario.rut == token_data.rut))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

def require_role(role: str):
    async def role_checker(current_user: Usuario = Depends(get_current_user)):
        if current_user.rol != role:
            raise HTTPException(status_code=403, detail="Permisos insuficientes")
        return current_user
    return role_checker
