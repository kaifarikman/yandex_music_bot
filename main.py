import asyncio
import logging
import sys

from aiogram import Dispatcher

from bot.bot import bot
from bot.admin.handlers import router as admin_router
from bot.user.handlers import router as user_router
from db.db import create_tables
from db.default_db import create_default_db


async def main():
    await create_tables()
    await create_default_db()
    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(user_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.getLogger('sqlalchemy.engine.Engine').disabled = True
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
