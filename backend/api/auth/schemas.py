from pydantic import BaseModel, EmailStr

# for user login
class UserLoginSchema(BaseModel):
    id: int
    email: EmailStr
    password: str

# schema for token
class TokenInfoSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


