from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status

from src.core.di import (
    get_interactor_user_create,
    get_interactor_user_delete,
    get_interactor_user_list,
    get_interactor_user_receive,
)
from src.models.users import UserId
from src.schemas.users import User, UserIn, UserPagination
from src.services.users import UserCreate, UserDelete, UserList, UserReceive

router = APIRouter(prefix="/users")


@router.get(
    path="",
    name="users:list_users",
    description="list users",
    status_code=status.HTTP_200_OK,
    summary="list users",
    response_model=UserPagination,
    responses={
        "200": {
            "description": "user",
            "model": UserPagination,
        },
        "400": {
            "description": "Bad request",
        },
    },
)
async def receive_users(
    page: int = Query(default=1, description="page"),
    per_page: int = Query(default=10, description="per page"),
    service: UserList = Depends(get_interactor_user_list),
) -> UserPagination:
    user_pagination = await service.execute(page, per_page)

    return user_pagination


@router.get(
    path="/{user_id}",
    name="users:get_user",
    description="get user",
    status_code=status.HTTP_200_OK,
    summary="get users",
    response_model=User,
    responses={
        "200": {
            "description": "user",
            "model": User,
        },
        "404": {
            "description": "Not found",
        },
    },
)
async def get_user(
    user_id: Annotated[
        UserId,
        Path(
            title="user id",
        ),
    ],
    service: UserReceive = Depends(get_interactor_user_receive),
) -> User:
    user = await service.execute(user_id)
    return user


@router.post(
    path="",
    name="users:create_user",
    description="create user",
    status_code=status.HTTP_201_CREATED,
    summary="create users",
    response_model=User,
    responses={
        "201": {
            "description": "user",
            "model": User,
        },
        "400": {
            "description": "Bad request",
        },
    },
)
async def create_user(
    user_in: UserIn = Body(..., description="user for creating"),
    service: UserCreate = Depends(get_interactor_user_create),
) -> User:
    user = await service.execute(user_in)
    return user


@router.delete(
    path="/{user_id}",
    name="users:delete_user",
    description="delete user",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        "204": {
            "description": "user deleted",
        },
    },
)
async def delete_user(
    user_id: Annotated[
        UserId,
        Path(
            title="user id",
        ),
    ],
    service: UserDelete = Depends(get_interactor_user_delete),
) -> None:
    await service.execute(user_id)
