from datetime import timedelta

from core.config import settings

from fastapi import HTTPException, status

from .schemas import UserLoginSchema
from .utils import encode_jwt

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt_token(token_type: str,
                     payload: dict,
                     expire_timedelta: timedelta | None = None,
                     expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(payload)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserLoginSchema) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "email": user.email,
    }
    return create_jwt_token(token_type=ACCESS_TOKEN_TYPE,
                            payload=jwt_payload,
                            expire_minutes=settings.auth_jwt.access_token_expire_minutes)


def create_refresh_token(user: UserLoginSchema) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "email": user.email,
    }
    return create_jwt_token(token_type=REFRESH_TOKEN_TYPE,
                            payload=jwt_payload,
                            expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_minutes))


def validate_token_type(payload: dict, token_type: str) -> bool:
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect token type")
