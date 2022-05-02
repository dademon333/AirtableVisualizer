import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum, Text

from db.base import Base, get_enum_values


class EntityColumn(str, enum.Enum):
    NAME = 'name'
    type = 'type'
    SIZE = 'size'
    DESCRIPTION = 'description'
    STUDY_TIME = 'study_time'


class EntityUpdate(Base):
    __tablename__ = 'entities_updates'

    id = Column(Integer, primary_key=True)
    entity_id = Column(
        Integer,
        ForeignKey('entities.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    column = Column(
        Enum(EntityColumn, name='entity_column', values_callable=get_enum_values),
        nullable=False
    )
    old_value = Column(Text, nullable=False)
    new_value = Column(Text, nullable=False)
