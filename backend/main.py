from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession

from api import router as api_router
from core.config import settings
from contextlib import asynccontextmanager
import api.articles.models
import api.users.models
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startapp
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
from sqlalchemy import text

# liveness endpoint
@main_app.get("/health", tags=["health"])
async def health_check(db: AsyncSession = Depends(db_helper.session_getter)):
    try:
        await db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "ok"
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "database": "unavailable"
            }
        )

main_app.include_router(
    api_router,
    prefix=settings.api.prefix)

if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True,)
