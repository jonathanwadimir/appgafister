from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config import SECRET_KEY, ALGORITHM
from app.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        rol: str = payload.get("rol")
        if username is None or rol is None:
            raise credentials_exception
        return TokenData(username=username, rol=rol)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(required_rol: str):
    async def role_checker(user: TokenData = Depends(get_current_user)):
        if user.rol != required_rol:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado para rol '{user.rol}'. Se requiere rol '{required_rol}'."
            )
        return user
    return role_checker
