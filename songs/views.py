from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from database.models import Song
from database.queries import get_entity

songs_router = APIRouter(prefix='/songs')

templates = Jinja2Templates(directory="templates/songs")


@songs_router.get('/', response_class=HTMLResponse)
async def get_songs(request: Request):
    """Вью для получения списка песен"""
    songs: list[Song] = await get_entity(
        session=request.state.session,
        model=Song,
        execute=True
    )
    return templates.TemplateResponse(
        'index.html', {'request': request, 'songs': songs}
    )


@songs_router.get('/{pk}', response_class=HTMLResponse)
async def get_song(request: Request, pk: int):
    """Вью для получения песни по идентификатору"""
    song: Song = await get_entity(
        session=request.state.session,
        model=Song,
        execute=True,
        single=True,
        id_song=pk
    )

    return templates.TemplateResponse(
        'song_detail.html',
        {
            'request': request,
            'song': song,
            'song_duration': '{:.2f}'.format(
                song.duration / 60
            ).replace('.', ':')
        }
    )
