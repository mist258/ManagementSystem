from typing import List

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
    hashed_password: str # will be deleted
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
