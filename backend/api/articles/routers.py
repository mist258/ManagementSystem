from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.articles.schemas import (ArticleCreateSchema,
                                  ArticleUpdateSchema,
                                  ArticleFullResponseSchema)
from core.models import db_helper
from api.users.models import User
from api.users.dependencies import (require_user_and_superuser,
                                    require_article_owner_or_staff,
                                    require_article_owner_or_admin,
                                    )
from .services import (create_article,
                       update_article,
                       delete_article,
                       get_all_articles,
                       get_article_by_id)


article_router = APIRouter()

@article_router.post("", response_model=ArticleCreateSchema, status_code=status.HTTP_201_CREATED)
async def post_new_article(
        article: ArticleCreateSchema,
        db: AsyncSession = Depends(db_helper.session_getter),
        user: User = Depends(require_user_and_superuser)
) -> ArticleCreateSchema:
    return await create_article(db, article, user)


@article_router.put("/{article_id}", response_model=ArticleUpdateSchema, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def update_article_by_id(
        article_id: int,
        data : ArticleUpdateSchema,
        db: AsyncSession = Depends(db_helper.session_getter),
        user: User = Depends(require_article_owner_or_staff)
):
    return await update_article(db, article_id, data)


@article_router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article_by_id(
        article_id: int,
        db: AsyncSession = Depends(db_helper.session_getter),
        user: User = Depends(require_article_owner_or_admin)
):
    return await delete_article(db, article_id)


@article_router.get("", response_model=List[ArticleFullResponseSchema], status_code=status.HTTP_200_OK )
async def get_articles(db: AsyncSession = Depends(db_helper.session_getter)): # TODO set pagination
    return await get_all_articles(db)


@article_router.get("/{article_id}", response_model=ArticleFullResponseSchema, status_code=status.HTTP_200_OK )
async def get_single_article_by_id(article_id: int, db: AsyncSession = Depends(db_helper.session_getter)):
    return await get_article_by_id(db, article_id)
