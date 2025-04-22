import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Tuple
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password) -> str:
    return pwd_context.hash(password)


def create_token(data: Dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


def create_tokens(id: UUID) -> Tuple[str, str]:
    now = datetime.now(timezone.utc)
    access_token = create_token(data={
        "sub": str(id),
        "type": "access",
        "iat": int(now.timestamp()),
        "jti": str(uuid.uuid4()),
    }, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token(data={
        "sub": str(id),
        "type": "refresh",
        "iat": int(now.timestamp()),
        "jti": str(uuid.uuid4()),
    }, expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

    return access_token, refresh_token


def decode_token(token: str) -> Dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
