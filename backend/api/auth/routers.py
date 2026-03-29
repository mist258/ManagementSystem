from api.auth.dependencies import (
    get_current_active_user,
    get_current_auth_user_for_refresh,
    validate_auth_user,
)
from api.auth.schemas import TokenInfoSchema, UserLoginSchema
from api.auth.services import create_access_token, create_refresh_token
from api.users.models import User
from api.users.schemas import UserCreateSchema, UserRetrieveSchema
from api.users.services import create_casual_user
from core.models import db_helper

from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter()


@auth_router.post(
    "/sign_up",
    response_model=UserRetrieveSchema,
    summary="Sign up in system",
    description="User can sign up in system. Available for anyone",
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
    data: UserCreateSchema,
    db: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    return await create_casual_user(db=db, data=data)


@auth_router.post(
    "/login",
    response_model=TokenInfoSchema,
    summary="Login",
    description="User will receive pair of tokens: access & refresh. Available for anyone.",
    status_code=status.HTTP_200_OK,
)
def user_login(
    user: UserLoginSchema = Depends(validate_auth_user),
) -> TokenInfoSchema:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfoSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@auth_router.get(
    "/me",
    response_model=UserRetrieveSchema,
    summary="Get information about me",
    description="Available for authorized users",
    status_code=status.HTTP_200_OK,
)
def current_user(
    user: UserRetrieveSchema = Depends(get_current_active_user),
) -> UserRetrieveSchema:
    return user


@auth_router.post(
    "/refresh",
    response_model=TokenInfoSchema,
    summary="Get a new access token",
    description="User can get a new pair of tokens using refresh token. Available for authorized users",
    status_code=status.HTTP_200_OK,
)
def user_refresh(
    user: UserLoginSchema = Depends(get_current_auth_user_for_refresh),
) -> TokenInfoSchema:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfoSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )
