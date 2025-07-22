import bot.admin.utils as utils


def users_statistic(users):
    text = '📊 Статистика пользователей:\n\n'
    to_sort = []
    for user in users:
        if user.username:
            to_sort.append(
                [user.count, f'@{user.username}']
            )
        else:
            to_sort.append(
                [user.count, f'{user.peer_id}']
            )
    to_sort.sort(reverse=True)
    for count, name in to_sort:
        text += f'{name} загрузил {utils.decline_track(count)}\n'
    return text


def pretty_playlist(playlist):
    text = '🎵 Плейлист:\n'
    text += f'Название: {playlist.name}\n'
    text += f'Ссылка: {playlist.link}\n'
    return text


admin_start_text = '🔧 Панель администратора'
admin_no_access = '🚫 У вас нет доступа к административному разделу.'
rejected = '❌ Доступ отклонён.'
accepted = '✅ Доступ предоставлен.'
export_data_text = '📤 Что вы хотите выгрузить?'
not_available_playlists = '📂 Сейчас нет доступных плейлистов.'
available_playlists = '📁 Список доступных плейлистов:'
create_playlist_name = '📝 Введите название нового плейлиста:'
invalid_playlist_name = '⚠️ Название должно состоять только из текста.'
create_playlist_link = '🔗 Отправьте ссылку на плейлист из Яндекс Музыки:'
invalid_playlist_link = '🚫 Похоже, ссылка некорректна. Попробуйте снова.'
successfully_added = '✅ Плейлист успешно добавлен!'
new_playlist_name = '✏️ Введите новое название для плейлиста:'
new_playlist_name_added = '✅ Новое имя успешно сохранено.'
really_delete = '❗ Вы точно хотите удалить этот плейлист? Это действие необратимо.'
cancelled_deleting = '❎ Удаление отменено.'
access_deleting = '🗑️ Плейлист успешно удалён.'
