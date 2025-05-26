from datetime import datetime, timedelta, timezone
from typing import Optional
import warnings
import os

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Suppress passlib bcrypt warning
os.environ["PASSLIB_BUILTIN_BCRYPT"] = "enabled"
warnings.filterwarnings("ignore", category=UserWarning, module="passlib")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(
            timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
