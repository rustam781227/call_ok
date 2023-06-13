from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates


home_router = APIRouter(prefix='')

templates = Jinja2Templates(directory="templates/")


@home_router.get('/', response_class=HTMLResponse)
async def get_home(request: Request):
    """Вью для получения домашней страницы"""
    return templates.TemplateResponse(
        'base.html', {'request': request}
    )
