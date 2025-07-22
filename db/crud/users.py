from db.schemas import User as UserDB
from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.db import engine


async def create_user(user: User):
    async with AsyncSession(engine) as session:
        user_db = UserDB(**user.model_dump())
        session.add(user_db)
        await session.commit()
        await session.refresh(user_db)


async def read_user(peer_id: int):
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(UserDB).where(UserDB.peer_id == peer_id)
        )
        result = query.scalars().first()
        return result


async def edit_preference(peer_id: int, preference_: str):
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(UserDB).where(UserDB.peer_id == peer_id)
        )
        user = query.scalar_one()
        user.preference = preference_

        await session.commit()


async def edit_count(peer_id: int):
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(UserDB).where(UserDB.peer_id == peer_id)
        )
        user = query.scalar_one()
        count = user.count + 1
        user.count = count
        await session.commit()


async def get_users():
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(UserDB)
        )
        return query.scalars().all()
