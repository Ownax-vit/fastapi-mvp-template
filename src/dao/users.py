from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User, UserId


class UserDAO(ABC):
    @abstractmethod
    async def get(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def list(self, page: int, per_page: int) -> Sequence[User]:
        raise NotImplementedError


class UserDAOImpl(UserDAO):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, user_id: UserId) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self._session.delete(user)
        await self._session.commit()
        return None

    async def count(self) -> int:
        stmt = select(func.count()).select_from(User)
        result = await self._session.execute(stmt)
        return result.scalar_one() or 0

    async def list(self, page: int, per_page: int) -> Sequence[User]:
        stmt = select(User).offset((page - 1) * per_page).limit(per_page)
        result = await self._session.execute(stmt)
        return result.scalars().all()
