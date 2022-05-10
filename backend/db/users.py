import enum

from sqlalchemy import Column, Integer, String, Enum, DateTime, func, Index
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import text

from .base import Base, get_enum_values


class UserStatus(str, enum.Enum):
    USER = 'user'
    EDITOR = 'editor'
    ADMIN = 'admin'


user_status_weights = {
    None: 0,
    UserStatus.USER: 0,
    UserStatus.EDITOR: 10,
    UserStatus.ADMIN: 20
}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    status = Column(
        Enum(UserStatus, name='user_status', values_callable=get_enum_values),
        nullable=False,
        server_default=UserStatus.USER
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    db_changes = relationship(
        'ChangeLog',
        backref=backref('editor_data', lazy='joined', uselist=False)
    )

    __table_args__ = (
        Index('ix_users_email', text('LOWER(email)'), unique=True),
    )
