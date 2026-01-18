from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.db import database
from src.dao.users import UserDAOImpl
from src.services.users import UserDelete, UserList, UserReceive, UserCreate



def get_interactor_user_receive(
    session: AsyncSession = Depends(dependency=database.get_session),
) -> UserReceive:
    """
    Dependency injection for UserReceive service.
    """
    user_dao = UserDAOImpl(session)
    return UserReceive(user_dao)


def get_interactor_user_create(
    session: AsyncSession = Depends(dependency=database.get_session),
) -> UserCreate:
    """
    Dependency injection for UserReceive service.
    """
    user_dao = UserDAOImpl(session)
    return UserCreate(user_dao)


def get_interactor_user_list(
    session: AsyncSession = Depends(dependency=database.get_session),
) -> UserList:
    """
    Dependency injection for UserList service.
    """
    user_dao = UserDAOImpl(session)
    return UserList(user_dao)


def get_interactor_user_delete(
    session: AsyncSession = Depends(dependency=database.get_session),
) -> UserDelete:
    """
    Dependency injection for UserDelete service.
    """
    user_dao = UserDAOImpl(session)
    return UserDelete(user_dao)
