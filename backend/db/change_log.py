import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship, backref

from .base import Base, get_enum_values


class ChangeType(str, enum.Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'


class ChangedTable(str, enum.Enum):
    ENTITIES = 'entities'
    ENTITIES_CONNECTIONS = 'entities_connections'
    ENTITIES_TYPES_CONNECTIONS = 'entities_types_connections'
    HIDDEN_COURSES = 'hidden_courses'

    USERS = 'users'


class ChangeLog(Base):
    __tablename__ = 'change_log'

    id = Column(Integer, primary_key=True)
    editor_id = Column(
        Integer,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='SET NULL')
    )
    type = Column(
        Enum(ChangeType, name='change_type', values_callable=get_enum_values),
        nullable=False
    )
    table = Column(
        Enum(ChangedTable, name='changed_table', values_callable=get_enum_values),
        nullable=False
    )
    element_id = Column(Integer, nullable=False, index=True)
    parent_change_id = Column(
        Integer,
        ForeignKey('change_log.id', onupdate='CASCADE', ondelete='CASCADE'),
        index=True
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    dependent_changes = relationship(
        'ChangeLog',
        backref=backref('parent_change', remote_side=[id]),
        lazy='joined',
        join_depth=1
    )
    update_instance = relationship(
        'DbElementUpdate',
        backref='log_instance',
        lazy='joined',
        uselist=False
    )
    delete_instance = relationship(
        'ArchivedDbElement',
        backref='log_instance',
        lazy='joined',
        uselist=False
    )
