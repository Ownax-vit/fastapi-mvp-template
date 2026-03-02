from uuid import uuid4

import pytest

from src.dao.users import UserDAOImpl
from src.exceptions.users import UserNotFoundError
from src.models.users import User, UserId
from src.schemas.users import UserIn
from src.services.users import UserCreate, UserDelete, UserList, UserReceive


@pytest.mark.asyncio
async def test_user_create(db_session):
    """Test user creation."""
    dao = UserDAOImpl(db_session)
    service = UserCreate(dao)

    user_in = UserIn(name="Test User", stars=5, comment="Test comment")
    user = await service.execute(user_in)

    assert user.name == "Test User"
    assert user.stars == 5
    assert user.comment == "Test comment"
    assert user.id is not None
    assert user.created_at is not None


@pytest.mark.asyncio
async def test_user_receive(db_session):
    """Test user retrieval."""
    dao = UserDAOImpl(db_session)
    create_service = UserCreate(dao)
    receive_service = UserReceive(dao)

    # Create a user first
    user_in = UserIn(name="Test User", stars=5, comment="Test comment")
    created_user = await create_service.execute(user_in)

    # Retrieve the user
    received_user = await receive_service.execute(UserId(created_user.id))

    assert received_user.id == created_user.id
    assert received_user.name == "Test User"


@pytest.mark.asyncio
async def test_user_receive_not_found(db_session):
    """Test user retrieval when user doesn't exist."""
    dao = UserDAOImpl(db_session)
    service = UserReceive(dao)

    fake_id = UserId(uuid4())
    with pytest.raises(UserNotFoundError):
        await service.execute(fake_id)


@pytest.mark.asyncio
async def test_user_list(db_session):
    """Test user listing with pagination."""
    dao = UserDAOImpl(db_session)
    create_service = UserCreate(dao)
    list_service = UserList(dao)

    # Create multiple users
    for i in range(5):
        user_in = UserIn(name=f"User {i}", stars=i, comment=f"Comment {i}")
        await create_service.execute(user_in)

    # List users
    result = await list_service.execute(page=1, per_page=10)

    assert result.total == 5
    assert len(result.items) == 5
    assert result.page == 1
    assert result.per_page == 10


@pytest.mark.asyncio
async def test_user_list_pagination(db_session):
    """Test user listing with pagination."""
    dao = UserDAOImpl(db_session)
    create_service = UserCreate(dao)
    list_service = UserList(dao)

    # Create multiple users
    for i in range(5):
        user_in = UserIn(name=f"User {i}", stars=i, comment=f"Comment {i}")
        await create_service.execute(user_in)

    # List users with pagination
    result = await list_service.execute(page=1, per_page=2)

    assert result.total == 5
    assert len(result.items) == 2
    assert result.page == 1
    assert result.per_page == 2


@pytest.mark.asyncio
async def test_user_delete(db_session):
    """Test user deletion."""
    dao = UserDAOImpl(db_session)
    create_service = UserCreate(dao)
    delete_service = UserDelete(dao)
    receive_service = UserReceive(dao)

    # Create a user
    user_in = UserIn(name="Test User", stars=5, comment="Test comment")
    created_user = await create_service.execute(user_in)

    # Delete the user
    await delete_service.execute(UserId(created_user.id))

    # Try to retrieve the user (should raise error)
    with pytest.raises(UserNotFoundError):
        await receive_service.execute(UserId(created_user.id))


@pytest.mark.asyncio
async def test_user_delete_not_found(db_session):
    """Test user deletion when user doesn't exist."""
    dao = UserDAOImpl(db_session)
    service = UserDelete(dao)

    fake_id = UserId(uuid4())
    with pytest.raises(UserNotFoundError):
        await service.execute(fake_id)

