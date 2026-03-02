from uuid import uuid4

import pytest

from src.schemas.users import UserIn


@pytest.mark.asyncio
async def test_create_user(client):
    """Test creating a user via API."""
    user_data = {
        "name": "Test User",
        "stars": 5,
        "comment": "Test comment",
    }

    response = await client.post("/api/v1/users", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["stars"] == 5
    assert data["comment"] == "Test comment"
    assert "id" in data
    assert "createdAt" in data


@pytest.mark.asyncio
async def test_get_user(client):
    """Test getting a user via API."""
    # Create a user first
    user_data = {
        "name": "Test User",
        "stars": 5,
        "comment": "Test comment",
    }
    create_response = await client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]

    # Get the user
    get_response = await client.get(f"/api/v1/users/{user_id}")

    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == user_id
    assert data["name"] == "Test User"


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    """Test getting a non-existent user."""
    fake_id = str(uuid4())
    response = await client.get(f"/api/v1/users/{fake_id}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_list_users(client):
    """Test listing users via API."""
    # Create multiple users
    for i in range(3):
        user_data = {
            "name": f"User {i}",
            "stars": i,
            "comment": f"Comment {i}",
        }
        await client.post("/api/v1/users", json=user_data)

    # List users
    response = await client.get("/api/v1/users/all?page=1&per_page=10")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3
    assert data["page"] == 1
    assert data["perPage"] == 10


@pytest.mark.asyncio
async def test_list_users_pagination(client):
    """Test listing users with pagination."""
    # Create multiple users
    for i in range(5):
        user_data = {
            "name": f"User {i}",
            "stars": i,
            "comment": f"Comment {i}",
        }
        await client.post("/api/v1/users", json=user_data)

    # List users with pagination
    response = await client.get("/api/v1/users/all?page=1&per_page=2")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["perPage"] == 2


@pytest.mark.asyncio
async def test_delete_user(client):
    """Test deleting a user via API."""
    # Create a user first
    user_data = {
        "name": "Test User",
        "stars": 5,
        "comment": "Test comment",
    }
    create_response = await client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]

    # Delete the user
    delete_response = await client.delete(f"/api/v1/users/{user_id}")

    assert delete_response.status_code == 204

    # Try to get the user (should fail)
    get_response = await client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_not_found(client):
    """Test deleting a non-existent user."""
    fake_id = str(uuid4())
    response = await client.delete(f"/api/v1/users/{fake_id}")

    assert response.status_code == 404

