from typing import List, Sequence

from api.articles.schemas import ArticleCreateSchema, ArticleFullResponseSchema, ArticleUpdateSchema
from api.users.dependencies import (
    require_article_owner_or_admin,
    require_article_owner_or_staff,
    require_user_and_superuser,
)
from api.users.models import User
from core.models import db_helper
from utils.pagination import PaginationDep

from fastapi import APIRouter, Depends, Query, status

from sqlalchemy.ext.asyncio import AsyncSession

from .enums import ArticleSortField, SortOrder
from .services import create_article, delete_article, get_all_articles, get_article_by_id, search_articles, update_article

article_router = APIRouter()

@article_router.get("", response_model=List[ArticleFullResponseSchema], status_code=status.HTTP_200_OK )
async def get_articles(pagination: PaginationDep,
        db: AsyncSession = Depends(db_helper.session_getter)):
    return await get_all_articles(pagination=pagination, db=db)

@article_router.get("/search", response_model=List[ArticleFullResponseSchema], status_code=status.HTTP_200_OK )
async def get_articles(pagination: PaginationDep,
                       db: AsyncSession = Depends(db_helper.session_getter),
                       search: str | None = Query(None, description="Search for articles"),
                       sort_by: ArticleSortField = Query(ArticleSortField.created_at),
                       sort_order: SortOrder = Query(SortOrder.desc),
) -> Sequence[ArticleFullResponseSchema]:
    return await search_articles(
        db=db,
        pagination=pagination,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order)

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


@article_router.get("/{article_id}", response_model=ArticleFullResponseSchema, status_code=status.HTTP_200_OK )
async def get_single_article_by_id(article_id: int, db: AsyncSession = Depends(db_helper.session_getter)):
    return await get_article_by_id(db, article_id)

