from typing import List, Sequence

from core.models import db_helper
from utils.pagination import PaginationDep

from fastapi import APIRouter, Depends, Query, status

from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import require_owner_or_superuser, require_superuser
from .models import User
from .schemas import EditorRetrieveSchema, UserCreateSchema, UserProfileBlockSchema, UserRetrieveSchema, UserUpdateSchema
from .services import (
    block_user,
    create_casual_user,
    create_editor,
    delete_user,
    get_all_users,
    get_all_users_editors,
    get_user_by_id,
    search_users_by_name,
    unblock_user,
    update_user,
)

users_router = APIRouter()

@users_router.get("/search", response_model=List[UserRetrieveSchema],
                  summary="Search user",
                  description="Search user by first or last name. Available for anyone."
                  )
async def search_users(
    pagination: PaginationDep,
    db: AsyncSession = Depends(db_helper.session_getter),
    search: str | None = Query(None, description="Search users by name"),
) -> Sequence[User]:
    return await search_users_by_name(db=db, pagination=pagination, search=search)


@users_router.get("/authors", response_model=List[UserRetrieveSchema],
                  summary="Get all authors",
                  description="Get all authors. Available for admin.",
                  status_code=status.HTTP_200_OK)
async def get_users_as_author(
        pagination: PaginationDep,
        db: AsyncSession = Depends(db_helper.session_getter),
        user: User = Depends(require_superuser)
):
    users = await get_all_users(db=db, pagination=pagination)
    return users


@users_router.get("/editors", response_model=List[EditorRetrieveSchema],
                    summary="Get all editors",
                    description="Get all editors. Available for admin.",
                    status_code=status.HTTP_200_OK)
async def get_users_as_editor(
        pagination: PaginationDep,
        db: AsyncSession = Depends(db_helper.session_getter),
        user: User = Depends(require_superuser)
):
    users = await get_all_users_editors(db=db, pagination=pagination)
    return users


@users_router.post("", response_model=UserRetrieveSchema,
                    summary="Create new user as author",
                    description="Available for admin.",
                    status_code=status.HTTP_201_CREATED)
async def create_user(
        data: UserCreateSchema,
        db: AsyncSession = Depends(db_helper.session_getter),
        user: User = Depends(require_superuser)
) -> User:
    return await create_casual_user(db=db, data=data)


@users_router.post("/editor", response_model=EditorRetrieveSchema,
                    summary="Create new user as editor",
                    description="Available for admin.",
                    status_code=status.HTTP_201_CREATED)
async def create_editor_user(
        data: UserCreateSchema,
        db: AsyncSession = Depends(db_helper.session_getter),
        user: User = Depends(require_superuser)
) -> User:
    return await create_editor(db=db, data=data)


@users_router.delete("/{user_id}",
                    summary="Delete user",
                    description="Delete any user by id. Available for admin.",
                    status_code=status.HTTP_204_NO_CONTENT )
async def delete_user_by_id(user_id: int,
                            db: AsyncSession = Depends(db_helper.session_getter),
                            user: User = Depends(require_superuser)) -> None:
    await delete_user(db=db, user_id=user_id)
    return None


@users_router.get("/{user_id}", response_model=UserRetrieveSchema,
                    summary="Get a single user",
                    description="Get user by id. Available for admin.",
                    status_code=status.HTTP_200_OK)
async def get_single_user(user_id: int,
                          db: AsyncSession = Depends(db_helper.session_getter),
                          user: User = Depends(require_superuser)) -> User:
    user = await get_user_by_id(db=db, user_id=user_id)
    return user


@users_router.patch("/{user_id}/block", response_model=UserProfileBlockSchema,
                    summary="Deactivate user",
                    description="Deactivate user by id. Available for admin.",
                    status_code=status.HTTP_200_OK)
async def deactivate_user(user_id: int,
                          db: AsyncSession = Depends(db_helper.session_getter),
                          user: User = Depends(require_superuser)) -> User:
    user = await block_user(db=db, user_id=user_id)
    return user


@users_router.patch("/{user_id}/unblock", response_model=UserProfileBlockSchema,
                    summary="Activate user",
                    description="Activate user by id. Available for admin.",
                    status_code=status.HTTP_200_OK)
async def activate_user(user_id: int,
                        db: AsyncSession = Depends(db_helper.session_getter),
                        user: User = Depends(require_superuser)) -> User:
    user = await unblock_user(db=db, user_id=user_id)
    return user


@users_router.put("/{user_id}", response_model=UserUpdateSchema,
                    summary="Update user",
                    description="Update user by id. Available for admin and account owner.",
                    status_code=status.HTTP_200_OK)
async def update_user_by_id(user_id: int,
                            data: UserUpdateSchema,
                            db: AsyncSession = Depends(db_helper.session_getter),
                            user: User = Depends(require_owner_or_superuser)
                            ) -> User:
    user = await update_user(data, db=db, user_id=user_id)
    return user

