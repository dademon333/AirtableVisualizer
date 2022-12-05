from auth.utils import hash_password
from infrastructure.db import User


def test_hash_password(user: User):
    result = hash_password(user_id=1, password="password")
    assert result == user.password
