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
from db.models import User, Playlist
import db.crud.users as crud_users
import db.crud.playlists as crud_playlists
import bot.admin.utils as utils
import os
from aiogram.types import FSInputFile

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
        count=0,
        preference='',
    )
    await crud_users.create_user(user)
    await bot.send_message(
        chat_id=peer_id,
        text=texts.accepted,
        reply_markup=await keyboards.user_start_use()
    )


@router.callback_query(F.data == "watch_statistic")
@is_admin
async def watch_statistic_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    users = await crud_users.get_users()
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.users_statistic(users),
        keyboard=await keyboards.back_button()
    )


@router.callback_query(F.data == 'export_data')
@is_admin
async def export_data_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    await send_callback_aiogram_message(
        callback=callback,
        text=texts.export_data_text,
        keyboard=await keyboards.export_data()
    )


@router.callback_query(F.data == 'export_users')
@is_admin
async def export_users_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()
    await state.clear()
    users = await crud_users.get_users()
    filename = 'bot/admin/users_export.xlsx'
    utils.export_users_to_excel_pandas(users, filename)

    await callback.message.answer_document(
        document=FSInputFile(filename),
        caption=f"Экспорт пользователей ({len(users)} записей)",
        reply_markup=await keyboards.back_button()
    )

    if os.path.exists(filename):
        os.remove(filename)


@router.callback_query(F.data == 'manage_playlists')
@is_admin
async def manage_playlists_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    playlists = await crud_playlists.get_playlists()
    if len(playlists) == 0:
        return await send_callback_aiogram_message(
            callback=callback,
            text=texts.not_available_playlists,
            keyboard=await keyboards.create_new_playlist()
        )
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.available_playlists,
        keyboard=await keyboards.get_playlists(playlists, 1)
    )


@router.callback_query(F.data == 'dummy')
async def dump_callback_function(callback: CallbackQuery, state: FSMContext):
    await callback.answer()


@router.callback_query(F.data.startswith('change_playlist_page_'))
@is_admin
async def change_playlist_page_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    page = int(callback.data.split("_")[-1])
    playlists = await crud_playlists.get_playlists()
    if len(playlists) == 0:
        return await callback.message.edit_reply_markup(
            reply_markup=await keyboards.create_new_playlist()
        )
    await callback.message.edit_reply_markup(
        reply_markup=await keyboards.get_playlists(playlists, page)
    )


class NewPlaylist(StatesGroup):
    name = State()
    link = State()


@router.callback_query(F.data == "create_playlist")
@is_admin
async def create_playlist_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    await send_callback_aiogram_message(
        callback=callback,
        text=texts.create_playlist_name,
        keyboard=await keyboards.cancel()
    )
    await state.set_state(NewPlaylist.name)


@router.message(NewPlaylist.name)
@is_admin
async def create_playlist_name(message: Message, state: FSMContext):
    if not message.text:
        return await send_message_aiogram_message(
            message=message,
            text=texts.invalid_playlist_name,
            keyboard=await keyboards.cancel()
        )
    playlist_name = message.text
    await state.update_data({"name": playlist_name})
    await send_message_aiogram_message(
        message=message,
        text=texts.create_playlist_link,
        keyboard=await keyboards.cancel()
    )
    await state.set_state(NewPlaylist.link)


@router.message(NewPlaylist.link)
@is_admin
async def create_playlist_link(message: Message, state: FSMContext):
    if not message.text:
        return await send_message_aiogram_message(
            message=message,
            text=texts.invalid_playlist_link,
            keyboard=await keyboards.cancel()
        )
    playlist_kind = utils.check_playlist_link(message.text)
    if not playlist_kind:
        return await send_message_aiogram_message(
            message=message,
            text=texts.invalid_playlist_link,
            keyboard=await keyboards.cancel()
        )
    playlist_name = (await state.get_data())['name']
    playlist_link = message.text
    await state.clear()
    playlist = Playlist(
        name=playlist_name,
        kind=playlist_kind,
        link=playlist_link
    )
    await crud_playlists.create_playlist(playlist)
    await send_message_aiogram_message(
        message=message,
        text=texts.successfully_added,
        keyboard=await keyboards.to_playlists()
    )


@router.callback_query(F.data.startswith('playlist_id_'))
@is_admin
async def playlist_id_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    playlist_id = int(callback.data.split("_")[-1])
    playlist = await crud_playlists.read_playlist(playlist_id)
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.pretty_playlist(playlist),
        keyboard=await keyboards.change_playlist_settings(playlist_id)
    )


class NewPlaylistName(StatesGroup):
    playlist_id = State()
    name = State()


@router.callback_query(F.data.startswith('change_playlist_name_'))
@is_admin
async def change_playlist_name_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    playlist_id = int(callback.data.split('_')[-1])
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.new_playlist_name,
        keyboard=await keyboards.to_main_playlist(playlist_id)
    )
    await state.set_state(NewPlaylistName.name)
    await state.update_data({'playlist_id': playlist_id})


@router.message(NewPlaylistName.name)
@is_admin
async def new_playlist_name_message(message: Message, state: FSMContext):
    if not message.text:
        return await send_message_aiogram_message(
            message=message,
            text=texts.invalid_playlist_name,
            keyboard=await keyboards.cancel()
        )
    playlist_name = message.text
    playlist_id = (await state.get_data())['playlist_id']
    await state.clear()
    await crud_playlists.change_name(playlist_id, playlist_name)
    await send_message_aiogram_message(
        message=message,
        text=texts.new_playlist_name_added,
        keyboard=await keyboards.to_playlists()
    )


@router.callback_query(F.data.startswith('delete_playlist_'))
@is_admin
async def delete_playlist_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    playlist_id = int(callback.data.split('_')[-1])
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.really_delete,
        keyboard=await keyboards.really_delete(playlist_id)
    )


@router.callback_query(F.data.startswith('playlist_delete_'))
@is_admin
async def playlist_delete_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    callback_data = callback.data.split('_')
    if callback_data[2] == 'cancel':
        return await send_callback_aiogram_message(
            callback=callback,
            text=texts.cancelled_deleting,
            keyboard=await keyboards.to_main_playlist(int(callback_data[-1]))
        )
    await crud_playlists.delete_playlist(int(callback_data[-1]))
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.access_deleting,
        keyboard=await keyboards.to_playlists()
    )