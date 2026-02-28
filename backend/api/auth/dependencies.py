from fastapi import Form, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from core.models import db_helper
from jwt import InvalidTokenError
from sqlalchemy import select
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .utils import validate_password, decode_jwt
from api.users.models import User, UserProfile
from api.users.schemas import UserRetrieveSchema
from .services import ACCESS_TOKEN_TYPE, validate_token_type, REFRESH_TOKEN_TYPE

http_bearer = HTTPBearer()

async def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
    db:AsyncSession = Depends(db_helper.session_getter)
):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise unauthed_exception

    if not validate_password(
            password=password,
            hashed_password=user.hashed_password,
    ):
        raise unauthed_exception

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Inactive user")
    return user

# get payload
async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                           detail="Invalid token")
    return payload


async def get_user_by_token_sub(
        payload: dict,
        db: AsyncSession
) -> UserRetrieveSchema:

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")
    result = await (db.execute(
        select(User)
        .options(
            joinedload(User.profile)
            .selectinload(UserProfile.articles)
        )
        .where(User.id == int(user_id)))
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found")
    return user

# access token
# todo can be something wrong with articles
async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(db_helper.session_getter)
):
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return await get_user_by_token_sub(payload, db)


# refresh token
async def get_current_auth_user_for_refresh(
        payload: dict = Depends(get_current_token_payload),
        db: AsyncSession = Depends(db_helper.session_getter)
):
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    return await get_user_by_token_sub(payload, db)


# check is user authorized
async def get_current_active_user(
    user: UserRetrieveSchema = Depends(get_current_auth_user)
):
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Inactive user")
    return user


