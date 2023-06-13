from pydantic import BaseModel


class RatingIn(BaseModel):
    id_song: int
    rating: int
