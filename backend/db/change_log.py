import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, func

from .base import Base, get_enum_values


class ChangeType(str, enum.Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'


class ChangeLog(Base):
    __tablename__ = 'change_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='SET NULL'),
        nullable=False,
        index=True
    )
    type = Column(
        Enum(ChangeType, name='change_type', values_callable=get_enum_values),
        nullable=False
    )
    entity_id = Column(
        Integer,
        ForeignKey('entities.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())
