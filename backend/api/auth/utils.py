from datetime import UTC, datetime, timedelta, timezone

import bcrypt
import jwt
from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
) -> str:
    """
    Create JWT token
    """
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta

    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)

    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)  # generate token
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    """
    Decode JWT token
    """
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> str:
    """
    Password hashing
    """
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()  # turn password into bytes
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def validate_password(password: str, hashed_password: str) -> bool:
    """
    Check the match of the received password with the hashed password
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
