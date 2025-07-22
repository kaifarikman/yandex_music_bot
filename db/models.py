from pydantic import BaseModel


class User(BaseModel):
    peer_id: int
    username: str | None
    count: int
    preference: str


class Admin(BaseModel):
    peer_id: int


class Playlist(BaseModel):
    name: str
    kind: int
    link: str
