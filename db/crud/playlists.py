from db.schemas import Playlist as PlaylistDB
from db.models import Playlist
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.db import engine


async def create_playlist(playlist: Playlist):
    async with AsyncSession(engine) as session:
        playlist_db = PlaylistDB(**playlist.model_dump())
        session.add(playlist_db)
        await session.commit()
        await session.refresh(playlist_db)


async def read_playlist(id_: int):
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(PlaylistDB).where(PlaylistDB.id == id_)
        )
        result = query.scalars().first()
        return result


async def change_name(playlist_id: int, playlist_name: str):
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(PlaylistDB).where(PlaylistDB.id == playlist_id)
        )
        result = query.scalars().first()
        result.name = playlist_name
        await session.commit()


async def delete_playlist(playlist_id: int):
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(PlaylistDB).where(PlaylistDB.id == playlist_id)
        )
        playlist = query.scalars().first()
        if playlist:
            await session.delete(playlist)
            await session.commit()


async def get_playlists():
    async with AsyncSession(engine) as session:
        query = await session.execute(
            select(PlaylistDB)
        )
        result = query.scalars().all()
        return result
