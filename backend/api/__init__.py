from fastapi import APIRouter

from .articles.routers import article_router
from .auth.routers import auth_router
from .users.routers import users_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(article_router, prefix="/articles", tags=["articles"])
