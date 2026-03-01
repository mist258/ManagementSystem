from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence
from sqlalchemy.orm.exc import StaleDataError

from api.articles.models import Article
from api.users.models import User
from api.articles.schemas import ArticleCreateSchema, ArticleUpdateSchema


async def create_article(
        db:AsyncSession,
        article: ArticleCreateSchema,
        user:User
):
    """
        can create: user & superuser
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


async def get_all_articles(db: AsyncSession) -> Sequence[Article]:
    """
        can get: anyone
    """
    result = await db.execute(
        select(Article)
    )
    return result.scalars().all()


async def get_article_by_id(db:AsyncSession, article_id: int) -> Article:
    """
         can get: anyone
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


# todo search users and articles
