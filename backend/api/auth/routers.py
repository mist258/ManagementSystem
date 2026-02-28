from fastapi import APIRouter, Depends
from .utils import encode_jwt
from .schemas import UserLoginSchema, TokenInfoSchema
from .dependencies import validate_auth_user
auth_router = APIRouter()

@auth_router.post("/login", response_model=TokenInfoSchema)
async def user_login(
        user: UserLoginSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.id,
        "email": user.email,
    }
    token = encode_jwt(jwt_payload)
    return TokenInfoSchema(
        access_token=token,
        token_type="Bearer",
    )
