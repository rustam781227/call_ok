from fastapi import APIRouter
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from starlette.status import HTTP_201_CREATED
from fastapi.templating import Jinja2Templates

from database.models import Playlist, SongInPlaylist
from database.queries import get_entity
from database.utils import try_flush_commit
from playlists.schema import PlaylistIn, PlaylistSongsIn

playlist_router = APIRouter(prefix='/playlists')

templates = Jinja2Templates(directory="templates/playlists")


@playlist_router.get('/', response_class=HTMLResponse)
async def get_playlists(request: Request):
    """Вью для получения списка песен"""
    playlists: list[Playlist] = await get_entity(
        session=request.state.session,
        model=Playlist,
        execute=True
    )
    return templates.TemplateResponse(
        'index.html', {'request': request, 'playlists': playlists}
    )


@playlist_router.post('/', status_code=HTTP_201_CREATED)
async def create_playlist(request: Request, playlist: PlaylistIn) -> None:
    """Вью для создания нового плейлиста"""
    playlist = Playlist(name=playlist.name)
    request.state.session.add(playlist)
    await try_flush_commit(session=request.state.session, commit=True)


@playlist_router.post('/{pk}/songs', status_code=HTTP_201_CREATED)
async def add_songs(request: Request, pk: int,
                    playlist_songs: PlaylistSongsIn) -> None:
    """Вью для добавления новой песни в плейлист"""
    for id_song in playlist_songs.songs:
        request.state.session.add(
            SongInPlaylist(id_song=id_song, id_playlist=pk)
        )
    await try_flush_commit(session=request.state.session, commit=True)
