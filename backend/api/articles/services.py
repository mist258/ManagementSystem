from api.articles.models import Article
from api.articles.schemas import ArticleCreateSchema, ArticleUpdateSchema
from api.users.models import User
from utils.pagination import PaginationDep

from fastapi import HTTPException, status

from sqlalchemy import Sequence, asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import StaleDataError

from .enums import ArticleSortField, SortOrder


async def create_article(
        db:AsyncSession,
        article: ArticleCreateSchema,
        user:User
):
    """
        can create: user & superuser
        :param: db[AsyncSession]
        :param: article[schema]
        :param: user
    """
    result = Article(
        title=article.title,
        content=article.content,
        author_id=user.profile.id
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


async def update_article(
        db:AsyncSession,
        article_id: int,
        data: ArticleUpdateSchema,
) -> ArticleCreateSchema:
    """
        can update: owner & editor & superuser
        :param: db[AsyncSession]
        :param: article_id[int]
        :param: data
    """
    result = await db.execute(
        select(Article).where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Article not found")

    if data.title is not None:
        article.title = data.title

    if data.content is not None:
        article.content = data.content

    try:
        await db.commit()
    except StaleDataError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Article was modified by someone else")
    await db.refresh(article)
    return article


async def delete_article(db: AsyncSession, article_id: int) -> None:
    """
        can delete: owner & superuser
        :param: db[AsyncSession]
        :param: article_id[int]
    """
    result = await db.execute(
        select(Article).where(Article.id == article_id)
    )

    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Article not found")

    await db.delete(article)
    await db.commit()


async def get_all_articles(
        pagination: PaginationDep,
        db: AsyncSession) -> Sequence[Article]:
    """
        can get: anyone
        :param: db[AsyncSession]
        :param: pagination
    """
    result = await db.execute(
        select(Article)
        .limit(pagination.limit)
        .offset(pagination.offset)
    )
    return result.scalars().all()


async def get_article_by_id(
        db:AsyncSession,
        article_id: int) -> Article:
    """
        can get: anyone
        :param: db[AsyncSession]
        :param: article_id[int]
    """
    result = await db.execute(
        select(Article)
        .where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Article not found")
    return article


async def search_articles(
        db:AsyncSession,
        pagination: PaginationDep,
        search: str | None = None,
        sort_by: ArticleSortField = ArticleSortField.created_at,
        sort_order: SortOrder = SortOrder.desc,
) -> Sequence[Article]:
    """
        can get: anyone
        :param: db[AsyncSession]
        :param: pagination
        :param: search[str] or None
        :param: sort_by[ArticleSortField]
        :param: sort_order[ArticleSortField]
    """

    stmt = select(Article)

    if search:
        stmt = stmt.where(Article.title.ilike(f"%{search}%"))

    sort_column = getattr(Article, sort_by.value)

    if sort_order == SortOrder.desc:
        stmt = stmt.order_by(desc(sort_column))
    else:
        stmt = stmt.order_by(asc(sort_column))

    stmt = stmt.limit(pagination.limit).offset(pagination.offset)

    result = await db.execute(stmt)
    return result.scalars().all()


