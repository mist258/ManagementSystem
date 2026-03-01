from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from fastapi import HTTPException
from .schemas import UserCreateSchema, UserUpdateSchema
from sqlalchemy.orm import joinedload
from .models import User, UserProfile
from sqlalchemy import select
from api.auth.utils import hash_password
from utils.pagination import PaginationDep

async def create_casual_user(db:AsyncSession, data: UserCreateSchema) -> User:
    """
        can create: admin
    """
    try:
        db_user = User(
            email=data.email,
            hashed_password=hash_password(data.hashed_password),
            is_active=True,
            is_staff=False,
        )
        db.add(db_user)
        await db.flush()

        db_profile = UserProfile(
            user_id=db_user.id,
            first_name=data.profile.first_name,
            last_name=data.profile.last_name,
        )
        db.add(db_profile)
        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    result = await db.execute(
        select(User)
        .options(joinedload(User.profile)
                 .selectinload(UserProfile.articles))
        .where(User.id == db_user.id)
    )
    return result.scalar_one()


async def create_editor(db:AsyncSession, data: UserCreateSchema ) -> User:
    """
        can create: admin
    """

    try:
        db_user = User(
            email=data.email,
            hashed_password=hash_password(data.hashed_password),
            is_active=True,
            is_staff=False,
        )
        db.add(db_user)
        await db.flush()

        db_profile = UserProfile(
            user_id=db_user.id,
            first_name=data.profile.first_name,
            last_name=data.profile.last_name,
        )
        db.add(db_profile)
        await db.commit()

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    result = await db.execute(
        select(User)
        .options(joinedload(User.profile)
                 .selectinload(UserProfile.articles))
        .where(User.id == db_user.id)
    )
    return result.scalar_one()


async def get_all_users(db:AsyncSession,
                        pagination: PaginationDep) -> Sequence[User]: # have to set pagination todo
    """
        return all users and a titles of their articles
        can get: admin only
    """
    result = await db.execute(
        select(User)
        .options(
            joinedload(User.profile)
            .selectinload(UserProfile.articles)
        )
        .where(User.is_staff == False)
        .limit(pagination.limit)
        .offset(pagination.offset)
    )
    return result.unique().scalars().all() # 'unique()' because of 'joinedload()' can duplicate

async def get_all_users_editors(db:AsyncSession,
                                pagination: PaginationDep) -> Sequence[User]: # have to set pagination todo
    """
        return all users and a titles of their articles
        can get: admin only
    """
    result = await db.execute(
        select(User)
        .options(
            joinedload(User.profile)
            .selectinload(UserProfile.articles)
        )
        .where(User.is_staff == True)
        .where(User.is_superuser == False)
        .limit(pagination.limit)
        .offset(pagination.offset)
    )
    return result.unique().scalars().all()

async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    """
        can get: admin only
    """
    result = await db.execute(
        select(User)
        .options(
            joinedload(User.profile)
            .selectinload(UserProfile.articles)
        )
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def update_user(data: UserUpdateSchema, db: AsyncSession, user_id: int, ) -> User:
    """
        can update: admin & account's owner
    """
    result = await db.execute(
        select(User)
        .options(
            joinedload(User.profile)
        )
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_update = data.model_dump(exclude_unset=True)

    if "profile" in user_update:
        profile_data = user_update.pop("profile")
        for key, value in profile_data.items():
            setattr(user.profile, key, value)

    for key, value in user_update.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession,
                      user_id: int):
    """
        Delete user
        :param: user_id
        :return: None
        :permission: admin
    """
    result = select(User).where(User.id == user_id)
    user = await db.scalar(result)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()


async def block_user(db: AsyncSession, user_id: int) -> User: # soft deletion
    """
        Deactivate user
        :param: user_id
        :return: blocked user
        :permission: admin
    """
    result = await db.execute(
        select(User)
        .options(
            joinedload(User.profile)
        )
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_superuser:
        raise HTTPException(status_code=403, detail="Cannot block superuser")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="User already deactivated")

    user.is_active = False
    await db.commit()
    await db.refresh(user)
    return user


async def unblock_user(db: AsyncSession, user_id: int) -> User:
    """
        :param user_id:
        :return: unblocked user
        :permission: admin
    """
    result = await db.execute(
        select(User)
        .options(
            joinedload(User.profile)
        )
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_active:
        raise HTTPException(status_code=400, detail="User already activated")

    user.is_active = True
    await db.commit()
    await db.refresh(user)
    return user
