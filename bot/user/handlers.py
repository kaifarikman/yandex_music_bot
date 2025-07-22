from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.user.utils import is_registered
from bot.default_functions import send_callback_aiogram_message, send_message_aiogram_message

import bot.user.texts as texts
import bot.user.keyboards as keyboards
import bot.user.utils as utils
import db.crud.admins as crud_admins
import db.crud.users as crud_users
import db.crud.playlists as crud_playlists
from bot.bot import bot
from services.yandex_music_service import add_track_to_playlist

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


@router.callback_query(F.data == 'support')
@is_registered
async def support_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    await send_callback_aiogram_message(
        callback=callback,
        text=texts.help_text,
        keyboard=await keyboards.settings_menu()
    )


@router.callback_query(F.data == 'my_preferences')
@is_registered
async def my_preferences_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    peer_id = int(callback.from_user.id)
    user = await crud_users.read_user(peer_id)
    if user.preference == '':
        return await send_callback_aiogram_message(
            callback=callback,
            text=texts.no_preferences,
            keyboard=await keyboards.add_preference()
        )
    preference = user.preference
    return await send_callback_aiogram_message(
        callback=callback,
        text=texts.done_preference(preference),
        keyboard=await keyboards.manage_preference()
    )


class Preference(StatesGroup):
    pref = State()


@router.callback_query(F.data == 'add_my_preference')
@is_registered
async def add_preferences_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    await send_callback_aiogram_message(
        callback=callback,
        text=texts.add_preferences,
        keyboard=await keyboards.back_button()
    )
    await state.set_state(Preference.pref)


@router.message(Preference.pref)
@is_registered
async def preference_message(message: Message, state: FSMContext):
    if not message.text:
        return await send_message_aiogram_message(
            message=message,
            text=texts.invalid_preference,
            keyboard=await keyboards.back_button()
        )
    peer_id = message.from_user.id
    preference = message.text + '\n'
    await crud_users.edit_preference(peer_id, preference)
    await send_message_aiogram_message(
        message=message,
        text=texts.preference_added(preference),
        keyboard=await keyboards.manage_preference()
    )
    await state.clear()


class PreferencePlus(StatesGroup):
    pref = State()


@router.callback_query(F.data == 'add_more_preference')
@is_registered
async def add_my_preference_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    await send_callback_aiogram_message(
        callback=callback,
        text=texts.add_more_preference,
        keyboard=await keyboards.cancel_keyboard()
    )
    await state.set_state(PreferencePlus.pref)


@router.message(PreferencePlus.pref)
@is_registered
async def preference_plus_message(message: Message, state: FSMContext):
    if not message.text:
        return await send_message_aiogram_message(
            message=message,
            text=texts.invalid_preference,
            keyboard=await keyboards.back_button()
        )
    peer_id = message.from_user.id
    preference = message.text + '\n'
    user_preference = (await crud_users.read_user(peer_id)).preference
    new_pref = user_preference + preference
    await crud_users.edit_preference(peer_id, new_pref)
    await send_message_aiogram_message(
        message=message,
        text=texts.preference_added(new_pref),
        keyboard=await keyboards.manage_preference()
    )
    await state.clear()


@router.callback_query(F.data == "add_track")
@is_registered
async def add_track_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    playlists = await crud_playlists.get_playlists()

    if len(playlists) == 0:
        return await send_callback_aiogram_message(
            callback=callback,
            text=texts.not_available_playlists,
            keyboard=await keyboards.back_button()
        )
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.available_playlists,
        keyboard=await keyboards.get_playlists(playlists, 1)
    )


@router.callback_query(F.data.startswith('change_user_playlist_page_'))
@is_registered
async def change_playlist_page_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    page = int(callback.data.split("_")[-1])
    playlists = await crud_playlists.get_playlists()
    await callback.message.edit_reply_markup(
        reply_markup=await keyboards.get_playlists(playlists, page)
    )


class LastPlaylist(StatesGroup):
    playlist_id = State()
    link = State()


@router.callback_query(F.data.startswith('user_playlist_id_'))
@is_registered
async def user_playlist_id_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    playlist_id = int(callback.data.split('_')[-1])
    playlist = await crud_playlists.read_playlist(playlist_id)
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.pretty_playlist(playlist),
        keyboard=await keyboards.add_tracks(playlist_id)
    )


@router.callback_query(F.data.startswith('add_track_to_'))
@is_registered
async def add_track_to_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    playlist_id = int(callback.data.split('_')[-1])
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.send_track_to_playlist,
        keyboard=await keyboards.to_playlist(playlist_id)
    )
    await state.set_state(LastPlaylist.link)
    await state.update_data({'playlist_id': playlist_id})


@router.message(LastPlaylist.link)
@is_registered
async def last_playlist_link_message(message: Message, state: FSMContext):
    playlist_id = (await state.get_data())['playlist_id']
    if not message.text:
        return await send_message_aiogram_message(
            message=message,
            text=texts.invalid_link,
            keyboard=await keyboards.to_playlist(playlist_id)
        )
    extracting = utils.extract_ids(message.text)
    if extracting == "no format":
        return await send_message_aiogram_message(
            message=message,
            text=texts.invalid_link,
            keyboard=await keyboards.to_playlist(playlist_id)
        )
    if extracting == "album link":
        return await send_message_aiogram_message(
            message=message,
            text=texts.invalid_link_no_album,
            keyboard=await keyboards.to_playlist(playlist_id)
        )
    album_id, track_id = map(int, extracting)
    playlist = await crud_playlists.read_playlist(playlist_id)
    playlist_kind = playlist.kind
    response = add_track_to_playlist(album_id, track_id, playlist_kind)
    if response == 'already added':
        return await send_message_aiogram_message(
            message=message,
            text=texts.already_added,
            keyboard=await keyboards.go_to_playlist(playlist_id)
        )
    await crud_users.edit_count(message.from_user.id)
    return await send_message_aiogram_message(
        message=message,
        text=texts.successfully_added,
        keyboard=await keyboards.go_to_playlist(playlist_id)
    )


@router.callback_query(F.data == "show_video")
@is_registered
async def show_video_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_reply_markup()

    await callback.message.answer_video(
        video="BAACAgIAAxkBAAIBkWh-0RfM9vdRuZU3ldNY3f8ZA0FyAALjgAACzeDwSwkr0vdymJegNgQ",
        caption=texts.something_like_this,
        reply_markup=await keyboards.back_button(),
    )
