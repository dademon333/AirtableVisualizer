from fastapi import Request
from fastapi.templating import Jinja2Templates

from config import Config

graph_templates = Jinja2Templates(directory=Config.GRAPH_FRONT_ROOT)
table_templates = Jinja2Templates(directory=Config.TABLE_FRONT_ROOT)


async def html_page_middleware(request: Request, call_next):
    """Returns project html page on GET requests with 'accept': 'text/html' header.

    GET requests to api with 'accept': 'application/json' (or other) skips forward.

    """
    if request.method == 'GET' \
            and 'text/html' in request.headers.get('accept', '')\
            and request.url.path not in [request.app.docs_url, request.app.redoc_url]:
        if request.url.path.startswith('/table'):
            return table_templates.TemplateResponse(
                'index.html', {'request': request}
            )
        else:
            return graph_templates.TemplateResponse(
                'index.html', {'request': request}
            )

    return await call_next(request)
