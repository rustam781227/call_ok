from pydantic import BaseModel


class PlaylistIn(BaseModel):
    name: str


class PlaylistSongsIn(BaseModel):
    songs: list[int]
