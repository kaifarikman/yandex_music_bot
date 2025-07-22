from bot.default_functions import generate_keyboard


async def admin_keyboard():
    buttons = [
        ('Управлять плейлистами', 'manage_playlists'),
        ('Посмотреть статистику', 'watch_statistic'),
        ('Экспорт данных', 'export_data'),
        # ('Управлять админами', 'manage_admins')
    ]
    layout = [1, 2]
    return await generate_keyboard(buttons, layout)


async def back_button():
    buttons = [
        ('В главное меню', 'admin')
    ]
    layout = [1]
    return await generate_keyboard(buttons, layout)


async def to_user_menu():
    buttons = [
        ('В главное меню', 'start')
    ]
    layout = [1]
    return await generate_keyboard(buttons, layout)


async def user_start_use():
    buttons = [
        ('Начинайте пользоваться!', 'start')
    ]
    layout = [1]
    return await generate_keyboard(buttons, layout)


async def export_data():
    buttons = [
        # ('Плейлисты', 'export_playlists'),
        ('Пользователей', 'export_users'),
        ('В главное меню', 'admin')
    ]
    layout = [1, 1]
    return await generate_keyboard(buttons, layout)


async def create_new_playlist():
    buttons = [
        ('Создать плейлист', 'create_playlist'),
        ('Выйти в меню', 'admin')
    ]
    layout = [1, 1]
    return await generate_keyboard(buttons, layout)


async def cancel():
    buttons = [
        ('Отменить', 'admin'),
    ]
    layout = [1, ]
    return await generate_keyboard(buttons, layout)


async def to_playlists():
    buttons = [
        ('К плейлистам', 'manage_playlists'),
        ('В меню', 'admin')
    ]
    layout = [1, 1]
    return await generate_keyboard(buttons, layout)


async def get_playlists(playlists, page):
    static_count = 5
    buttons = []
    for playlist in playlists:
        buttons.append(
            (playlist.name, f"playlist_id_{playlist.id}")
        )
    pages_count = (
        len(playlists) // static_count + 1
        if len(playlists) % static_count != 0
        else len(playlists) // static_count
    )
    left_page = page - 1 if page != 1 else pages_count
    right_page = page + 1 if page != pages_count else 1
    configuration_field = [
        ("⬅️", f"change_playlist_page_{left_page}"),
        (f"{page} из {pages_count}", "dummy"),
        ("➡️", f"change_playlist_page_{right_page}"),
        ('Создать плейлист', 'create_playlist'),
        ('В меню', 'admin')
    ]
    layout = [1] * len(buttons)
    buttons += configuration_field
    layout += [3, 1, 1]
    return await generate_keyboard(buttons, layout)


async def change_playlist_settings(playlist_id):
    buttons = [
        ('Сменить название', f'change_playlist_name_{playlist_id}'),
        ('Удалить', f'delete_playlist_{playlist_id}'),
        ('Выйти обратно', 'manage_playlists'),
    ]
    layout = [2, 1]
    return await generate_keyboard(buttons, layout)


async def to_main_playlist(playlist_id):
    buttons = [
        ('Обратно', f'playlist_id_{playlist_id}'),
    ]
    layout = [1]
    return await generate_keyboard(buttons, layout)


async def really_delete(playlist_id):
    buttons = [
        ('Да', f'playlist_delete_totally_{playlist_id}'),
        ('Нет', f'playlist_delete_cancel_{playlist_id}')
    ]
    layout = [2]
    return await generate_keyboard(buttons, layout)
