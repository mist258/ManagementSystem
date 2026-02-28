from fastapi import APIRouter, Depends
from starlette import status

from .utils import encode_jwt
from .schemas import UserLoginSchema, TokenInfoSchema
from .dependencies import validate_auth_user, get_current_active_user
from api.users.schemas import UserRetrieveSchema


auth_router = APIRouter()

@auth_router.post("/login", response_model=TokenInfoSchema, status_code=status.HTTP_200_OK)
async def user_login(
        user: UserLoginSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": str(user.id),
        "email": user.email,
    }
    token = encode_jwt(jwt_payload)
    return TokenInfoSchema(
        access_token=token,
        token_type="Bearer",
    )

@auth_router.get("/me", response_model=UserRetrieveSchema, status_code=status.HTTP_200_OK)
async def current_user(user: UserRetrieveSchema = Depends(get_current_active_user)):
    return user