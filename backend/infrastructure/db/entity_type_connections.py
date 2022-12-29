from sqlalchemy import Column, Integer, Enum, String, UniqueConstraint

from infrastructure.db.base import Base, get_enum_values
from infrastructure.db.entities import EntityType


class EntityTypeConnection(Base):
    __tablename__ = 'entity_type_connections'

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

    __table_args__ = (
        UniqueConstraint('parent_type', 'child_type'),
    )
