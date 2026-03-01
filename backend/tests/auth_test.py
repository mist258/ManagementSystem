import pytest
from api.auth.utils import hash_password
from api.users.models import User
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_success(db_session, client):
    # створюємо юзера
    user = User(
        email="user1@test.com",
        hashed_password=hash_password("User123!"),
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()

    # робимо запит на login
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "email": "user1@test.com",
            "password": "User123!"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

async def test_login_wrong_password(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "email": "user1@test.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

async def test_login_wrong_email(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "email": "notexist@test.com",
            "password": "User123!"
        }
    )
    assert response.status_code == 401