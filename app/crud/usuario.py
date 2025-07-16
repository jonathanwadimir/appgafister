from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.models.usuario import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_user_by_username(db: AsyncSession, username: str) -> Usuario | None:
    result = await db.execute(select(Usuario).where(Usuario.username == username))
    return result.scalars().first()

async def create_user(db: AsyncSession, username: str, password: str, rol: str = "cliente") -> Usuario:
    hashed_password = get_password_hash(password)
    new_user = Usuario(username=username, hashed_password=hashed_password, rol=rol)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
