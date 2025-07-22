from bot.default_functions import generate_keyboard


async def start_keyboard():
    buttons = [
        ('Добавить трек', 'add_track'),
        ('Мои предпочтения', 'my_preferences'),
        ('Помощь', 'support')
    ]
    layout = [1, 1, 1]
    return await generate_keyboard(buttons, layout)


async def register_keyboard():
    buttons = [
        ('Зарегистрироваться', 'register_me')
    ]
    layout = [1]
    return await generate_keyboard(buttons, layout)


async def get_register_keyboard(peer_id):
    buttons = [
        ('Да', f'statement_accept_{peer_id}'),
        ('Нет', f'statement_reject_{peer_id}')
    ]
    layout = [2]
    return await generate_keyboard(buttons, layout)


async def back_button():
    buttons = [
        ('В главное меню', 'start'),
    ]
    layout = [1]
    return await generate_keyboard(buttons, layout)


async def add_preference():
    buttons = [
        ('Добавить предпочтения', 'add_my_preference'),
        ('В главное меню', 'start'),
    ]
    layout = [1, 1]
    return await generate_keyboard(buttons, layout)


async def manage_preference():
    buttons = [
        ('Дополнить', 'add_more_preference'),
        ('Заполнить заново', 'add_my_preference'),
        ('В главное меню', 'start'),
    ]
    layout = [2, 1]
    return await generate_keyboard(buttons, layout)


async def cancel_keyboard():
    buttons = [
        ('Отменить', 'my_preferences')
    ]
    layout = [1]
    return await generate_keyboard(buttons, layout)


async def get_playlists(playlists, page):
    static_count = 5
    buttons = []
    for playlist in playlists:
        buttons.append(
            (playlist.name, f"user_playlist_id_{playlist.id}")
        )
    pages_count = (
        len(playlists) // static_count + 1
        if len(playlists) % static_count != 0
        else len(playlists) // static_count
    )
    left_page = page - 1 if page != 1 else pages_count
    right_page = page + 1 if page != pages_count else 1
    configuration_field = [
        ("⬅️", f"change_user_playlist_page_{left_page}"),
        (f"{page} из {pages_count}", "dummy"),
        ("➡️", f"change_user_playlist_page_{right_page}"),
        ('В меню', 'start')
    ]
    layout = [1] * len(buttons)
    buttons += configuration_field
    layout += [3, 1]
    return await generate_keyboard(buttons, layout)


async def add_tracks(playlist_id):
    buttons = [
        ('Добавить трек в плейлист', f'add_track_to_{playlist_id}'),
        ('Выйти', 'add_track'),
    ]
    layout = [1, 1]
    return await generate_keyboard(buttons, layout)


async def to_playlist(playlist_id):
    buttons = [
        ('Отменить', f'user_playlist_id_{playlist_id}')
    ]
    layout = [1]
    return await generate_keyboard(buttons, layout)


async def go_to_playlist(playlist_id):
    buttons = [
        ('К плейлисту', f'user_playlist_id_{playlist_id}')
    ]
    layout = [1]
    return await generate_keyboard(buttons, layout)


async def settings_menu():
    buttons = [
        ('Посмотреть видео туториал', 'show_video'),
        ('В главное меню', 'start')
    ]
    layout = [1, 1]
    return await generate_keyboard(buttons, layout)
