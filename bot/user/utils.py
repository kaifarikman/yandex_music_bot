from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import db.crud.users as crud_users
from bot.default_functions import send_callback_aiogram_message, send_message_aiogram_message

import bot.user.texts as texts
import bot.user.keyboards as keyboards


def is_registered(func):
    async def wrapper(message: Message | CallbackQuery, state: FSMContext):
        peer_id = int(message.from_user.id)
        if await crud_users.read_user(peer_id):
            return await func(message, state)
        else:
            if isinstance(message, Message):
                return await send_message_aiogram_message(
                    message=message,
                    text=texts.register_me,
                    keyboard=await keyboards.register_keyboard()
                )
            return await send_callback_aiogram_message(
                callback=message,
                text=texts.register_me,
                keyboard=await keyboards.register_keyboard()
            )

    return wrapper
