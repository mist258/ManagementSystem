from httpx import AsyncClient


async def test_get_all_users(client: AsyncClient, admin_token: str):
    response = await client.get(
        "/api/v1/users/authors",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_user_by_id(client: AsyncClient, admin_token: str, create_test_user):
    response = await client.get(
        f"/api/v1/users/{create_test_user.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "user1@test.com"


async def test_get_user_by_id_not_found(client: AsyncClient, admin_token: str):
    response = await client.get(
        "/api/v1/users/999",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404


async def test_create_user(client: AsyncClient, admin_token: str):
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "newuser@test.com",
            "hashed_password": "NewUser123!",
            "profile": {"first_name": "New", "last_name": "User"}
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201


async def test_create_user_duplicate_email(client: AsyncClient, admin_token: str, create_test_user):
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "user1@test.com",
            "hashed_password": "User123!",
            "profile": {"first_name": "John", "last_name": "Doe"}
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400


async def test_block_user(client: AsyncClient, admin_token: str, create_test_user):
    response = await client.patch(
        f"/api/v1/users/{create_test_user.id}/block",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["is_active"] == False


async def test_get_users_unauthorized(client: AsyncClient):
    response = await client.get("/api/v1/users/authors")
    assert response.status_code == 401