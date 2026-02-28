from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from .schemas import UserRetrieveSchema, UserCreateSchema, EditorRetrieveSchema, UserProfileBlockSchema
from fastapi import APIRouter, Depends, status
from .models import User
from .services import (get_all_users,
                       create_casual_user,
                       create_editor,
                       delete_user,
                       get_user_by_id,
                       block_user,
                       unblock_user,
                       update_user)

users_router = APIRouter()

@users_router.get("", response_model=List[UserRetrieveSchema], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(db_helper.session_getter)
): # should set pagination todo
    users = await get_all_users(db=db)
    return users


@users_router.post("", response_model=UserRetrieveSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
        user: UserCreateSchema,
        db: AsyncSession = Depends(db_helper.session_getter)
) -> User:
    return await create_casual_user(db=db, user=user)


@users_router.post("/editor", response_model=EditorRetrieveSchema, status_code=status.HTTP_201_CREATED)
async def create_editor_user(
        user: UserCreateSchema,
        db: AsyncSession = Depends(db_helper.session_getter)
) -> User:
    return await create_editor(db=db, user=user)


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT )
async def delete_user_by_id(user_id: int, db: AsyncSession = Depends(db_helper.session_getter)) -> None:
    await delete_user(db=db, user_id=user_id)
    return None


@users_router.get("/{user_id}", response_model=UserRetrieveSchema, status_code=status.HTTP_200_OK)
async def get_single_user(user_id: int, db: AsyncSession = Depends(db_helper.session_getter)) -> User:
    user = await get_user_by_id(db=db, user_id=user_id)
    return user


@users_router.patch("/{user_id}/block", response_model=UserProfileBlockSchema, status_code=status.HTTP_200_OK)
async def deactivate_user(user_id: int, db: AsyncSession = Depends(db_helper.session_getter)) -> User:
    user = await block_user(db=db, user_id=user_id)
    return user


@users_router.patch("/{user_id}/unblock", response_model=UserProfileBlockSchema, status_code=status.HTTP_200_OK)
async def activate_user(user_id: int, db: AsyncSession = Depends(db_helper.session_getter)) -> User:
    user = await unblock_user(db=db, user_id=user_id)
    return user

@users_router.put("/{user_id}", response_model=UserCreateSchema, status_code=status.HTTP_200_OK)
async def update_user_by_id(user_id: int, data:UserCreateSchema, db: AsyncSession = Depends(db_helper.session_getter)) -> User:
    user = await update_user(data, db=db, user_id=user_id)
    return user








