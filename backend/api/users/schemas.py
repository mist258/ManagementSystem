from typing import List
import re
from pydantic import BaseModel, EmailStr, field_validator
from api.articles.schemas import ArticleTitleSchema

# for casual user
class UserProfileRetrieveSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    articles: List[ArticleTitleSchema] = []


class UserRetrieveSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_staff: bool
    is_superuser: bool
    profile: UserProfileRetrieveSchema

# for editor
class EditorProfileRetrieveSchema(BaseModel):
    id: int
    first_name: str
    last_name: str

class EditorRetrieveSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_staff: bool
    profile: EditorProfileRetrieveSchema


# create editor and casual user
class UserProfileSchema(BaseModel):
    first_name: str
    last_name: str


class UserCreateSchema(BaseModel):
    email: EmailStr
    hashed_password: str
    profile: UserProfileSchema

    @field_validator('email')
    @classmethod
    def normalize_email(cls, email: EmailStr) -> EmailStr:

        email_name, domain_part = email.strip().rsplit('@', 1)
        email = email_name + "@" + domain_part.lower()
        return email

    @field_validator('hashed_password')
    @classmethod
    def validate_received_password(cls, password: str) -> str:

        pattern = r"^[A-Za-z\d@$!%*?&]{8,}$"

        if not re.fullmatch(pattern, password):
            raise ValueError('Password must contain at least 8 characters,'
                                    '1 special symbol, 1 letter, 1 number')
        return password

# update user
class UserUpdateSchema(BaseModel):
    email: EmailStr
    profile: UserProfileSchema

    @field_validator('email')
    @classmethod
    def normalize_email(cls, email: EmailStr) -> EmailStr:

        email_name, domain_part = email.strip().rsplit('@', 1)
        email = email_name + "@" + domain_part.lower()
        return email

# for blocking & unblocking users
class UserBlockUnblockSchema(BaseModel):
    id: int
    first_name: str
    last_name: str


class UserProfileBlockSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_staff: bool
    profile: UserBlockUnblockSchema

