import enum

from sqlalchemy import Column, Integer, String, Enum, DateTime, func

from .base import Base, get_enum_values


class UserStatus(str, enum.Enum):
    USER = 'user'
    EDITOR = 'editor'
    ADMIN = 'admin'


user_status_weights = {
    UserStatus.USER: 0,
    UserStatus.EDITOR: 10,
    UserStatus.ADMIN: 20
}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True, unique=True)
    password = Column(String, nullable=False)
    status = Column(
        Enum(UserStatus, name='user_status', values_callable=get_enum_values),
        nullable=False,
        server_default=UserStatus.USER
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())
