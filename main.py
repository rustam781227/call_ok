from typing import Callable

from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse

from database.base import create_session
from database.utils import try_flush_commit
from home.views import home_router
from playlists.views import playlist_router
from ratings.views import rating_router
from songs.views import songs_router

colloquium = FastAPI(
    title='Colloquium_Salpagarov',
    description='',
    version='0.1',
)

colloquium.mount("/static", StaticFiles(directory="static"), name="static")


async def session_maker(request: Request, call_next: Callable) -> Response:
    """
    Middleware для добавления объекта сессии в объект
    запроса для дальнейшего использования.
    :param:         request - объект HTTP-запроса
    :param:         call_next - функция для передачи запроса в приложение
    """
    session = create_session()
    request.state.session = session
    try:
        response = await call_next(request)
    except SQLAlchemyError as ex:
        await request.state.session.rollback()
        return JSONResponse(
            content={
                'detail': ' '.join(arg for arg in ex.args)
            },
            status_code=HTTP_400_BAD_REQUEST
        )
    await try_flush_commit(session=request.state.session, commit=True)
    await request.state.session.close()
    return response


colloquium.add_middleware(
    middleware_class=BaseHTTPMiddleware,
    dispatch=session_maker
)

colloquium.include_router(router=songs_router, prefix='')
colloquium.include_router(router=playlist_router, prefix='')
colloquium.include_router(router=rating_router, prefix='')
colloquium.include_router(router=home_router, prefix='')
