from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.user.utils import is_registered
from bot.default_functions import send_callback_aiogram_message, send_message_aiogram_message

import bot.user.texts as texts
import bot.user.keyboards as keyboards
import db.crud.admins as crud_admins
from bot.bot import bot


router = Router()


@router.message(CommandStart())
@is_registered
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    await send_message_aiogram_message(
        message=message,
        text=texts.start_text,
        keyboard=await keyboards.start_keyboard()
    )


@router.callback_query(F.data == 'start')
@is_registered
async def start_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.start_text,
        keyboard=await keyboards.start_keyboard()
    )


@router.callback_query(F.data == "register_me")
async def register_me_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()

    admins = await crud_admins.get_all_admins()
    peer_id = int(callback.from_user.id)
    username = callback.from_user.username
    msg = texts.get_register_message(username, peer_id)
    kb = await keyboards.get_register_keyboard(peer_id)
    for admin_id in admins:
        await bot.send_message(
            chat_id=admin_id,
            text=msg,
            reply_markup=kb
        )
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.send_to_review,
    )