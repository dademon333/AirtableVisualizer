from sqlalchemy import Column, Integer, Enum, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base, get_enum_values
from .entity import EntityType


class EntitiesTypesConnection(Base):
    __tablename__ = 'entities_types_connections'

    id = Column(Integer, primary_key=True)
    parent_type = Column(
        Enum(EntityType, name='entity_type', values_callable=get_enum_values),
        nullable=False
    )
    child_type = Column(
        Enum(EntityType, name='entity_type', values_callable=get_enum_values),
        nullable=False
    )
    parent_column_name = Column(String)
    child_column_name = Column(String)

    entities_connections = relationship('EntitiesConnection', backref='types_connection', lazy='joined')

    __table_args__ = (
        UniqueConstraint('parent_type', 'child_type'),
    )
