from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import db.crud.admins as crud_admins
from bot.default_functions import send_callback_aiogram_message, send_message_aiogram_message

import bot.admin.texts as texts
import bot.admin.keyboards as keyboards


def is_admin(func):
    async def wrapper(message: Message | CallbackQuery, state: FSMContext):
        peer_id = int(message.from_user.id)
        if await crud_admins.read_admin(peer_id):
            return await func(message, state)
        else:
            if isinstance(message, Message):
                return await send_message_aiogram_message(
                    message=message,
                    text=texts.admin_no_access,
                    keyboard=await keyboards.to_user_menu()
                )
            return await send_callback_aiogram_message(
                callback=message,
                text=texts.admin_no_access,
                keyboard=await keyboards.to_user_menu()
            )

    return wrapper
