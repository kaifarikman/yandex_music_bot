def get_register_message(username, peer_id):
    if username is None:
        return f"👤 Пользователь с ID <code>{peer_id}</code> хочет зарегистрироваться. Принять?"
    return f"👤 Пользователь @{username} хочет зарегистрироваться. Принять?"


def done_preference(preferences):
    return f'🧠 Ваши текущие предпочтения:\n{preferences}\nХотите что-то изменить?'


def preference_added(preference):
    return f'✅ Предпочтение добавлено! Вы можете выйти или изменить его позже.\nТекущее значение:\n{preference}'


def pretty_playlist(playlist):
    text = '🎵 Плейлист:\n'
    text += f'Название: {playlist.name}\n'
    text += f'Ссылка: {playlist.link}\n'
    return text


start_text = '👋 Привет! Это бот для создания плейлистов.'
start_text += 'Сначала зарегистрируйся, а после, если ничего не понял, то тыкни в поддержку:))'
register_me = '🔐 Нажми сюда, чтобы зарегистрироваться'
send_to_review = '📤 Отправлено на модерацию'
help_text = '❓ Что-то сломалось? Напиши <a href="https://t.me/king_offkaif">сюда</a> — разберёмся!'
no_preferences = '📭 Пока что у вас нет предпочтений. Самое время добавить их!'
add_preferences = '📝 Введите ваше музыкальное предпочтение:'
invalid_preference = '⚠️ Только текст. Пожалуйста, попробуйте ещё раз.'
add_more_preference = '🧩 Напишите дополнение к предпочтению — оно будет добавлено.'
not_available_playlists = '📂 Пока что нет доступных плейлистов.'
available_playlists = '📁 Вот какие плейлисты доступны:'
send_track_to_playlist = '🎶 Отправьте ссылку на трек из Яндекс Музыки, чтобы добавить его в плейлист:'
invalid_link = '❌ Ссылка не распознана. Пожалуйста, отправьте корректную ссылку на трек.'
invalid_link_no_album = '🚫 Это ссылка на альбом. Пожалуйста, отправьте ссылку на конкретный трек.'
already_added = 'ℹ️ Этот трек уже есть в плейлисте.'
successfully_added = '✅ Трек успешно добавлен!'
something_like_this = 'Ну что-то такое, да. Возможно будет долго грузится, но так хотя бы понятнее будет'

