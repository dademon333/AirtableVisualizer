from typing import Callable, Any, NoReturn

import pytest

from auth.di import get_user_status, get_user_id_soft
from infrastructure.db import UserStatus, User


@pytest.fixture()
def editor_status_request(
        di_override: Callable[[Any, Any], NoReturn]
) -> NoReturn:
    """Overrides get_user_status dependency to return editor status."""
    di_override(get_user_status, UserStatus.EDITOR)


@pytest.fixture()
def admin_status_request(
        di_override: Callable[[Any, Any], NoReturn]
) -> NoReturn:
    """Overrides get_user_status dependency to return editor status."""
    di_override(get_user_status, UserStatus.ADMIN)


@pytest.fixture()
def get_user_id_override(
        user_admin: User,
        di_override: Callable[[Any, Any], NoReturn]
) -> int:
    di_override(get_user_id_soft, user_admin.id)
    return user_admin.id
