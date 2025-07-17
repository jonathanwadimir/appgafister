from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioOut, UsuarioCreate
from app.crud.usuario import obtener_usuario_por_rut, crear_usuario
from app.auth.auth import require_role, get_current_user
from pydantic import BaseModel

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.get("/solo-admin")
async def acceso_admin(current_user: Usuario = Depends(require_role("admin"))):
    return {"mensaje": f"Hola {current_user.rut}, tienes acceso como administrador."}

@router.get("/solo-tecnico")
async def acceso_tecnico(current_user: Usuario = Depends(require_role("tecnico"))):
    return {"mensaje": f"Hola {current_user.rut}, tienes acceso como técnico."}

@router.get("/solo-cliente")
async def acceso_cliente(current_user: Usuario = Depends(require_role("cliente"))):
    return {"mensaje": f"Hola {current_user.rut}, tienes acceso como cliente."}

@router.get("/cualquiera")
async def acceso_general(current_user: Usuario = Depends(get_current_user)):
    return {"mensaje": f"Hola {current_user.rut}, tu rol es: {current_user.rol}"}

@router.get("/", response_model=list[UsuarioOut])
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario))
    usuarios = result.scalars().all()
    return usuarios

@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
async def crear_usuario_endpoint(user: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    existente = await obtener_usuario_por_rut(db, user.rut)
    if existente:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    return await crear_usuario(db, user)

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario = result.scalar_one_or_none()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    await db.delete(usuario)
    await db.commit()

class UserUpdateRole(BaseModel):
    rol: str

@router.put("/{usuario_id}", response_model=UsuarioOut)
async def actualizar_rol_usuario(
    usuario_id: int,
    user_update: UserUpdateRole,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_role("admin"))
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

@router.get("/{usuario_id}", response_model=UsuarioOut)
async def obtener_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario = result.scalar_one_or_none()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
