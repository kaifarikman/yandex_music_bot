from config import YANDEX_TOKEN
from yandex_music import Client
import re
import random


def add_track_to_playlist(album_id, track_id, playlist_kind):
    client = Client(YANDEX_TOKEN).init()
    target_playlist = client.users_playlists(playlist_kind)
    existing_track_ids = set(track.id for track in target_playlist.tracks)
    print(existing_track_ids)
    print(track_id)
    if track_id in existing_track_ids:
        return "already added"

    tracks = target_playlist.tracks if hasattr(target_playlist, 'tracks') else []
    current_track_count = len(tracks)
    insert_position = random.randint(0, current_track_count)
    client.users_playlists_insert_track(
        kind=target_playlist.kind,
        track_id=track_id,
        album_id=album_id,
        at=insert_position,
        revision=target_playlist.revision
    )
    return "added"


# def extract_ids(url):
#     # Паттерн для ссылок вида:
#     # https://music.yandex.ru/album/1234567/track/7654321
#     # https://music.yandex.ru/album/1234567
#     pattern = r"album/(\d+)(?:/track/(\d+))?"
#     match = re.search(pattern, url)
#     if match:
#         album_id = match.group(1)  # Всегда есть, если ссылка корректная
#         track_id = match.group(2)  # Может быть None, если ссылка ведёт на альбом
#         return album_id, track_id
#     return None, None
#
#
# url = "https://music.yandex.ru/album/17554329/track/89480861?utm_source=desktop&utm_medium=copy_link"
# album_id, track_id = extract_ids(url)
# client = Client(YANDEX_TOKEN).init()
#
# playlist_url = "https://music.yandex.com/users/kna.zevs/playlists/1008?utm_medium=copy_link"
# playlist_kind = re.search(r"playlists/(\d+)", playlist_url).group(1)
#
# target_playlist = client.users_playlists(playlist_kind)
#
# existing_track_ids = [
#     f"{track.id}"
#     for track in target_playlist.tracks
# ]
#
# new_track_id = f"{track_id}"
# print(new_track_id)
# if new_track_id in existing_track_ids:
#     print(f"Трек {track_id} уже есть в плейлисте '{target_playlist.title}'!")
#     quit()
#
# tracks = target_playlist.tracks if hasattr(target_playlist, 'tracks') else []
# current_track_count = len(tracks)
# insert_position = random.randint(0, current_track_count)
# client.users_playlists_insert_track(
#     kind=target_playlist.kind,
#     track_id=track_id,
#     album_id=album_id,
#     at=insert_position,
#     revision=target_playlist.revision
# )
#
# print(f"Трек {track_id} добавлен в плейлист '{target_playlist.title}'!")
