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


