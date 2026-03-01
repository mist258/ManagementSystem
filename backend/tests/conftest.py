import asyncio

import pytest
import pytest_asyncio
from api.articles.models import Article
from api.auth.utils import hash_password
from api.users.models import User, UserProfile
from core.config import settings
from core.models.base import Base
from core.models.db_helper import db_helper
from httpx import ASGITransport, AsyncClient
from main import main_app

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

test_engine = create_async_engine(
    str(settings.db_test.url),
    echo=False,
    poolclass=NullPool,
)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with test_engine.connect() as conn:
        transaction = await conn.begin()

        session = AsyncSession(
            bind=conn,
            expire_on_commit=False,
        )
        yield session

        await session.close()
        await transaction.rollback()


@pytest_asyncio.fixture(scope="function")
async def create_test_user(db_session):
    user = User(
        email="user1@test.com",
        hashed_password=hash_password("User123!"),
        is_active=True,
        is_staff=False,
        is_superuser=False
    )
    db_session.add(user)
    await db_session.flush()

    profile = UserProfile(
        user_id=user.id,
        first_name="John",
        last_name="Doe"
    )
    db_session.add(profile)
    await db_session.commit()
    return user

@pytest_asyncio.fixture
async def auth_token(client: AsyncClient, create_test_user):
    login = await client.post(
        "/api/v1/auth/login",
        data={"email": "user1@test.com", "password": "User123!"}
    )
    return login.json()["access_token"]


@pytest_asyncio.fixture(scope="function")
async def client(db_session):

    async def override_db():
        yield db_session

    main_app.dependency_overrides[db_helper.session_getter] = override_db

    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url="http://test",
    ) as ac:
        yield ac

    main_app.dependency_overrides.clear()

@pytest_asyncio.fixture(scope="function")
async def create_superuser(db_session):
    user = User(
        email="admin@test.com",
        hashed_password=hash_password("Admin123!"),
        is_active=True,
        is_staff=True,
        is_superuser=True
    )
    db_session.add(user)
    await db_session.flush()
    profile = UserProfile(user_id=user.id, first_name="Admin", last_name="Admin")
    db_session.add(profile)
    await db_session.commit()
    return user


@pytest_asyncio.fixture
async def admin_token(client: AsyncClient, create_superuser):
    login = await client.post(
        "/api/v1/auth/login",
        data={"email": "admin@test.com", "password": "Admin123!"}
    )
    return login.json()["access_token"]