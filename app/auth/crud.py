from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.usuario import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(Usuario).filter(Usuario.username == username))
    return result.scalars().first()

async def create_user(db: AsyncSession, username: str, password: str, rol: str = "cliente"):
    hashed_password = pwd_context.hash(password)
    user = Usuario(username=username, hashed_password=hashed_password, rol=rol)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
