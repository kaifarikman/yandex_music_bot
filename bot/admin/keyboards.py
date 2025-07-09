from bot.default_functions import generate_keyboard


async def admin_keyboard():
    buttons = [
        ('Управлять плейлистами', 'manage_playlists'),
        ('Посмотреть статистику', 'watch_statistic'),
        ('Управлять админами', 'manage_admins')
    ]
    layout = [1, 1]
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
