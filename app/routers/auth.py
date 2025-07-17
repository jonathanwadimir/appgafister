from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.usuario import UsuarioCreate
from app.schemas.token import Token
from app.auth.auth import create_access_token
from app.crud.usuario import crear_usuario, autenticar_usuario

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crear_usuario(db, user)
    access_token = create_access_token(data={"sub": db_user.rut, "rol": db_user.rol})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    rut = form_data.username  # Usamos RUT como username
    user = await autenticar_usuario(db, rut, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    access_token = create_access_token(data={"sub": user.rut, "rol": user.rol})
    return {"access_token": access_token, "token_type": "bearer"}
