from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.usuario import UsuarioCreate, Token
from app.crud import usuario as crud_usuario
from app.auth.auth import create_access_token
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud_usuario.crear_usuario(db, user)
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud_usuario.autenticar_usuario(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
