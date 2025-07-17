from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def crear_usuario(db: AsyncSession, user: UsuarioCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = Usuario(
        rut=user.rut,
        nombre=user.nombre,
        email=user.email,
        hashed_password=hashed_password,
        rol=user.rol,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def autenticar_usuario(db: AsyncSession, rut: str, password: str):
    result = await db.execute(select(Usuario).where(Usuario.rut == rut))
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

async def obtener_usuario_por_rut(db: AsyncSession, rut: str):
    result = await db.execute(select(Usuario).where(Usuario.rut == rut))
    return result.scalar_one_or_none()
