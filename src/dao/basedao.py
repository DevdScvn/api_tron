from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class BaseDAO:
    model = None

    @classmethod
    async def get_objects_or_404(cls, session: AsyncSession, offset: int, limit: int):
        """
        Получить один объект из таблицы.

        Если нет объектов - получить ошибку 404.
        """
        query = select(cls.model).order_by(cls.model.id.desc()).offset(offset).limit(limit)
        result = await session.execute(query)
        if result := result.scalars().all():
            return result
        else:
            raise HTTPException(status_code=404, detail="Object not found")

    @classmethod
    async def create(cls, session: AsyncSession, **object_data: dict):
        """
        Создать объект в таблице.

        Если нет - вернуть 404 и сделать rollback.
        """
        query = insert(cls.model).values(**object_data).returning(cls.model)
        try:
            result = await session.execute(query)
            await session.commit()
            return result.scalars().first()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Object already exists"
            ) from None
