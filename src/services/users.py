from src.core.logging import get_logger
from src.dao.users import UserDAO
from src.exceptions.users import UserNotFoundError
from src.models.users import User as UserModel
from src.models.users import UserId
from src.schemas.users import User, UserIn, UserPagination


logger = get_logger(__name__)


class UserCreate:
    def __init__(self, dao: UserDAO):
        self._dao = dao

    async def execute(self, user: UserIn) -> User:
        user_model = UserModel(**user.model_dump())
        user_model = await self._dao.create(user_model)
        return User.model_validate(user_model)


class UserReceive:
    def __init__(self, dao: UserDAO):
        self._dao = dao

    async def execute(self, user_id: UserId) -> User:
        user_model = await self._dao.get(user_id)
        if not user_model:
            raise UserNotFoundError(user_id=str(user_id))

        return User.model_validate(user_model)


class UserList:
    def __init__(self, dao: UserDAO):
        self._dao = dao

    async def execute(self, page: int, per_page: int) -> UserPagination:
        users: list[User] = []
        count = await self._dao.count()
        if count:
            users_models = await self._dao.list(page=page, per_page=per_page)
            users = [
                User.model_validate(user_model) for user_model in users_models
            ]

        return UserPagination(
            items=users,
            total=count,
            page=page,
            per_page=per_page,
        )


class UserDelete:
    def __init__(self, dao: UserDAO):
        self._dao = dao

    async def execute(self, user_id: UserId) -> None:
        user_model = await self._dao.get(user_id)
        if not user_model:
            raise UserNotFoundError(user_id=str(user_id))

        await self._dao.delete(user_model)
