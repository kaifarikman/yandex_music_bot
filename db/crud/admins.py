from db.schemas import Admin as AdminDB
from db.models import Admin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.db import engine


async def create_admin(admin: Admin):
    async with AsyncSession(engine) as session:
        admin_db = AdminDB(**admin.model_dump())
        session.add(admin_db)
        await session.commit()
        await session.refresh(admin_db)


async def read_admin(peer_id: int):
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(AdminDB).where(AdminDB.peer_id == peer_id)
        )
        result = query.scalars().first()
        return result


async def get_all_admins():
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(AdminDB)
        )
        return [user.peer_id for user in query.scalars().all()]

