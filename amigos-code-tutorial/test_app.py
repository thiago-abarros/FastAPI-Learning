from fastapi.testclient import TestClient
from httpx import AsyncClient, AsyncHTTPTransport
from uuid import UUID

import pytest
from main import app, db
from models import User, Role, Gender

@pytest.mark.asyncio
async def test_create_user():
    """
    Test creating a new user.

    This test ensures that a new user is created and added to the database correctly.

    Returns:
        None.
    """
    user_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "gender": "female",
        "roles": ["user"]
    }

    user_id = "b5d1dffe-681d-42cf-8f90-609e63a2f35c"
    user_data["id"] = user_id
    async with AsyncClient() as client:
        response = await client.post("/api/users", json=user_data)

        assert response.status_code == 200
        assert response.json() == {"id": user_id}

        response = client.get("/api/users")
        db_users = [User(**user_data) for user_data in response.json()]

        assert any(user.id == UUID(user_id) for user in db_users)

        created_user = next(user for user in db_users if user.id == UUID(user_id))

        assert created_user == User(**user_data)
        assert created_user == user_data

@pytest.mark.asyncio
async def test_delete_user():
    """Test deleting a user from the API."""

    # Get an existing user
    user = db[0]

    # Delete the user and check the response
    async with AsyncClient(transport=AsyncHTTPTransport(app=app)) as client:
        response = await client.delete(f"/api/users/{user.id}")
        assert response.status_code == 200, "Status code should be 200 OK"

    # Verify the user is no longer in the database
    assert user.id not in [user.id for user in db], "User should no longer exist in the database"

    # Test deleting a non-existent user
    non_existent_user_id = UUID("b5d1dffe-681d-42cf-8f90-609e63a2f35c")
    async with AsyncClient(transport=AsyncHTTPTransport(app=app)) as client:
        response = await client.delete(f"/api/users/{non_existent_user_id}")
        assert response.status_code == 404, "Status code for deleting a non-existent user should be 404 NOT FOUND"

    # Test deleting an invalid user
    invalid_user_id = "invalid_id"
    async with AsyncClient(transport=AsyncHTTPTransport(app=app)) as client:
        response = await client.delete(f"/api/users/{invalid_user_id}")
        assert response.status_code == 422, "Status code for deleting an invalid user should be 422 UNPROCESSABLE ENTITY"
