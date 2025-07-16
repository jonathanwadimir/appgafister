# app/routers/usuario.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas import UserOut, UserCreate
from app.auth.crud import get_user_by_username, create_user
from app.auth.auth import require_role, get_current_user
from pydantic import BaseModel

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

# 🔐 Rutas protegidas por rol (deben ir antes de /{usuario_id})
@router.get("/solo-admin")
async def acceso_admin(current_user: Usuario = Depends(require_role("admin"))):
    return {"mensaje": f"Hola {current_user.username}, tienes acceso como administrador."}

@router.get("/solo-tecnico")
async def acceso_tecnico(current_user: Usuario = Depends(require_role("tecnico"))):
    return {"mensaje": f"Hola {current_user.username}, tienes acceso como técnico."}

@router.get("/solo-cliente")
async def acceso_cliente(current_user: Usuario = Depends(require_role("cliente"))):
    return {"mensaje": f"Hola {current_user.username}, tienes acceso como cliente."}

@router.get("/cualquiera")
async def acceso_general(current_user: Usuario = Depends(get_current_user)):
    return {"mensaje": f"Hola {current_user.username}, tu rol es: {current_user.rol}"}

# 🔓 CRUD de usuarios
@router.get("/", response_model=list[UserOut])
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario))
    usuarios = result.scalars().all()
    return usuarios

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def crear_usuario(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existente = await get_user_by_username(db, user.username)
    if existente:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    return await create_user(db, user.username, user.password, user.rol)

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario = result.scalar_one_or_none()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    await db.delete(usuario)
    await db.commit()

# PUT para actualizar el rol del usuario
class UserUpdateRole(BaseModel):
    rol: str

@router.put("/{usuario_id}", response_model=UserOut)
async def actualizar_rol_usuario(
    usuario_id: int,
    user_update: UserUpdateRole,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))  # Solo admin puede actualizar rol
):
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario = result.scalar_one_or_none()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if user_update.rol not in ("cliente", "tecnico", "admin"):
        raise HTTPException(status_code=400, detail="Rol inválido")

    usuario.rol = user_update.rol
    db.add(usuario)
    await db.commit()
    await db.refresh(usuario)
    return usuario

# ⚠️ Esta ruta debe ir al final para no interferir con otras rutas
@router.get("/{usuario_id}", response_model=UserOut)
async def obtener_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario = result.scalar_one_or_none()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
