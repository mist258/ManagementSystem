from api.users.schemas import UserRetrieveSchema
from starlette import status

from fastapi import APIRouter, Depends

from .dependencies import (
    get_current_active_user,
    get_current_auth_user_for_refresh,
    validate_auth_user,
)
from .schemas import TokenInfoSchema, UserLoginSchema
from .services import create_access_token, create_refresh_token

auth_router = APIRouter()

@auth_router.post("/login", response_model=TokenInfoSchema,
                    summary="Login",
                    description="User will receive pair of tokens: access & refresh. Available for anyone.",
                    status_code=status.HTTP_200_OK)
def user_login(
        user: UserLoginSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfoSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )

@auth_router.get("/me", response_model=UserRetrieveSchema,
                    summary="Get information about me",
                    description="Available for authorized users",
                    status_code=status.HTTP_200_OK)
def current_user(user: UserRetrieveSchema = Depends(get_current_active_user)):
    return user


@auth_router.post("/refresh", response_model=TokenInfoSchema,
                    summary="Get a new access token",
                    description="User can get a new pair of tokens using refresh token. Available for authorized users",
                    status_code=status.HTTP_200_OK)
def user_refresh(
        user: UserLoginSchema = Depends(get_current_auth_user_for_refresh)
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfoSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )

