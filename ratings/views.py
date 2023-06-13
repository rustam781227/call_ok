from fastapi import APIRouter
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED

from database.models import SongRating
from database.utils import try_flush_commit
from ratings.schema import RatingIn

rating_router = APIRouter(prefix='/ratings')


@rating_router.post('/', status_code=HTTP_201_CREATED)
async def rate_song(request: Request, rate: RatingIn) -> None:
    """Вью для добавления новой оценки песне"""
    request.state.session.add(
        SongRating(rating=rate.rating, id_song=rate.id_song)
    )
    await try_flush_commit(session=request.state.session, commit=True)
