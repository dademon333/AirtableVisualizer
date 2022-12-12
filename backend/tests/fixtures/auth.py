from typing import Callable, Any, NoReturn

import pytest

from auth.di import get_user_status
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
