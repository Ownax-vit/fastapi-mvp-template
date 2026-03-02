from urllib.parse import urlparse

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.connectors.genderize import Genderize
from src.dao.db import database
from src.dao.users import UserDAOImpl
from src.infrastructure.http_client import HTTPXClient, Url
from src.services.users import UserCreate, UserDelete, UserList, UserReceive


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

    url = Url(
        urlparse("https://api.genderize.io/")
    )  # TODO оказываетя сервис платный, заменить бесплатным аналогом
    genderize = Genderize(http_client=HTTPXClient(base_url=url))
    return UserCreate(user_dao, genderize=genderize)


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
