from fastapi import Form, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from sqlalchemy import select
from .utils import validate_password
from api.users.models import User


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

