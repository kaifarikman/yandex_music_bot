from pydantic import BaseModel


class User(BaseModel):
    peer_id: int
    username: str | None
    count: int


class Admin(BaseModel):
    peer_id: int
