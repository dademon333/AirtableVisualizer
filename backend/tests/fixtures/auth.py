from typing import Callable, Any, NoReturn

import pytest

from auth.di import get_user_status, get_user_id_soft
from infrastructure.db import UserStatus


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
def override_get_user_id(
        di_override: Callable[[Any, Any], NoReturn]
) -> Callable[[int], NoReturn]:
    def override(new_id: int) -> NoReturn:
        di_override(get_user_id_soft, new_id)
    return override
