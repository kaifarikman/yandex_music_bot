from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.admin.utils import is_admin
import bot.admin.texts as texts
import bot.admin.keyboards as keyboards
from bot.default_functions import send_message_aiogram_message, send_callback_aiogram_message
from bot.bot import bot
from db.models import User, Admin
import db.crud.users as crud_users

router = Router()


@router.message(Command("admin"))
@is_admin
async def admin_command(message: Message, state: FSMContext):
    await state.clear()
    await send_message_aiogram_message(
        message=message,
        text=texts.admin_start_text,
        keyboard=await keyboards.admin_keyboard()
    )


@router.callback_query(F.data == "admin")
@is_admin
async def admin_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.admin_start_text,
        keyboard=await keyboards.admin_keyboard()
    )


@router.callback_query(F.data.startswith('statement_'))
@is_admin
async def statement_manage_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_reply_markup()

    callback_data = callback.data.split('_')
    manage, peer_id = callback_data[1], int(callback_data[2])
    if manage == 'reject':
        return await bot.send_message(
            chat_id=peer_id,
            text=texts.rejected
        )
    username = (await bot.get_chat(peer_id)).username
    user = User(
        peer_id=peer_id,
        username=username,
        count=0
    )
    await crud_users.create_user(user)
    await bot.send_message(
        chat_id=peer_id,
        text=texts.accepted,
        reply_markup=await keyboards.user_start_use()
    )
