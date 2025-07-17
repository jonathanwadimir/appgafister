from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas import UserCreate, Token, UserOut  # Que coincida con schemas/usuario.py
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

# Resto igual
