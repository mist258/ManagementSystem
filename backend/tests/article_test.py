from httpx import AsyncClient


async def test_create_article_success(client: AsyncClient, create_test_user):
    login = await client.post(
        "/api/v1/auth/login",
        data={"email": "user1@test.com", "password": "User123!"}
    )
    token = login.json()["access_token"]

    response = await client.post(
        "/api/v1/articles",
        json={"title": "Test article", "content": "Test content"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test article"


async def test_get_all_articles(client: AsyncClient):
    response = await client.get("/api/v1/articles")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_article_by_id_not_found(client: AsyncClient):
    response = await client.get("/api/v1/articles/999")
    assert response.status_code == 404


async def test_create_article_unauthorized(client: AsyncClient):
    response = await client.post(
        "/api/v1/articles",
        json={"title": "Test", "content": "Content"}
    )
    assert response.status_code == 401