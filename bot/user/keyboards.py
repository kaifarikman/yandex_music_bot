from bot.default_functions import generate_keyboard


async def start_keyboard():
    buttons = [
        ('Добавить трек', 'add_track'),
        ('Помощь', 'support')
    ]
    layout = [1, 1]
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
