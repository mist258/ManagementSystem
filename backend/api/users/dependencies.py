from api.articles.models import Article
from api.auth.dependencies import get_current_active_user
from api.users.models import User
from core.models import db_helper

from fastapi import Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# permission exclude editors; allow casual users & admin
async def require_user_and_superuser(
    user: User = Depends(get_current_active_user)
) -> User:
    if user.is_staff and not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Permission denied")
    return user

# permission that allow owner & editor & admin update article; exclude user that is not article's owner
async def require_article_owner_or_staff(
        article_id: int,
        db: AsyncSession = Depends(db_helper.session_getter),
        user: User = Depends(get_current_active_user)
) -> User:
    result = await db.execute(
        select(Article).where(Article.id == article_id))

    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Article not found")

    if (user.is_staff and user.is_superuser) or (user.is_staff and not user.is_superuser):
        return user

    if article.author_id != user.profile.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not your article")

    return user

# permission that allow owner & admin delete article; exclude users that is not article's owner or is editor
async def require_article_owner_or_admin(
        article_id: int,
        db: AsyncSession = Depends(db_helper.session_getter),
        user: User = Depends(get_current_active_user)
) -> User:
    result = await db.execute(
        select(Article).where(Article.id == article_id))

    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Article not found")
    if user.is_superuser:
        return user

    if user.is_staff:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Permission denied")

    if article.author_id != user.profile.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not your article")

    return user

# admin only
async def require_superuser(
    user: User = Depends(get_current_active_user)
) -> User:
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Permission denied")
    return user


# owner or admin only
async def require_owner_or_superuser(
        user_id: int,
        current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.is_superuser:
        return current_user

    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permission denied")

    return current_user