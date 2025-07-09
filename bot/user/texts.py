def get_register_message(username, peer_id):
    if username is None:
        return f"Пользователь <code>{peer_id}</code> желает быть регнутым. принимаем?"
    return f"Пользователь @{username} желает быть регнутым. принимаем?"


start_text = 'дарова'
register_me = 'короче тыкай сюда, чтобы регнуться'
send_to_review = 'отправлено на модераторство'
