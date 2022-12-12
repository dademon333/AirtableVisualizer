import http.cookies
from enum import Enum


class ProjectCookies(str, Enum):
    """Cookie names, which are used in project."""

    SESSION_ID = 'session_id'


def get_delete_cookie_header(cookie_name: ProjectCookies) -> str:
    """Returns 'set-cookie' header with empty value.

    FastAPI's HTTPException does not have api to delete cookies,
    but it have headers arg. So, you can delete some cookies using
    'set-cookie' header e.g.:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={
            'set-cookie': get_delete_cookie_header(ProjectCookies.SESSION_ID)
        }
    )

    """
    cookie: http.cookies.BaseCookie = http.cookies.SimpleCookie()
    key = cookie_name.value
    cookie[key] = ''
    cookie[key]['max-age'] = 0
    cookie[key]['expires'] = 0
    cookie[key]['path'] = '/'
    cookie[key]['samesite'] = 'lax'
    return cookie.output(header='').strip()
