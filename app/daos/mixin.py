from typing import Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_model import Base

ModelType = TypeVar("ModelType", bound=Base)


class GetMixin(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, session: AsyncSession, **kwargs) -> ModelType | None:
        stmt = select(self.model)
        if kwargs:
            stmt = stmt.filter_by(**kwargs)
        return await session.scalar(stmt)

    async def get_objs(
        self, session: AsyncSession, **kwargs
    ) -> list[ModelType]:
        stmt = select(self.model)
        if kwargs:
            stmt = stmt.filter_by(**kwargs)
        return (await session.scalars(stmt)).all()

    async def get_objs_by_filter(
        self, session: AsyncSession, *args
    ) -> list[ModelType]:
        stmt = select(self.model)
        if args:
            stmt = stmt.where(*args)
        return (await session.scalars(stmt)).all()


class CreateMixin(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, session: AsyncSession, **kwargs) -> ModelType:
        model = self.model
        new_object = model(**kwargs)
        session.add(new_object)
        await session.flush()
        return new_object


class UpdateMixin(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def update(
        self, session: AsyncSession, allow_none: bool = False, **kwargs
    ) -> ModelType:
        for key, value in kwargs.items():
            if not allow_none and value is None:
                continue
            self.model.__setattr__(key, value)
        await session.flush()
        return self.model


class ModelMixin(
    GetMixin[ModelType], CreateMixin[ModelType], UpdateMixin[ModelType]
):
    pass
