import enum

from sqlalchemy import Column, Integer, String, Text, Enum, UniqueConstraint

from .base import Base, get_enum_values


class EntityType(str, enum.Enum):
    COURSE = 'course'
    THEME = 'theme'
    KNOWLEDGE = 'knowledge'
    QUANTUM = 'quantum'

    TARGET = 'target'
    METRIC = 'metric'
    TASK = 'task'

    ACTIVITY = 'activity'
    SKILL = 'skill'
    COMPETENCE = 'competence'
    PROFESSION = 'profession'
    SUOS_COMPETENCE = 'suos_competence'


class EntitySize(str, enum.Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'


class Entity(Base):
    __tablename__ = 'entities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(
        Enum(EntityType, name='entity_type', values_callable=get_enum_values),
        nullable=False
    )
    size = Column(
        Enum(EntitySize, name='entity_size', values_callable=get_enum_values),
        nullable=False,
        server_default=EntitySize.MEDIUM
    )
    description = Column(Text)
    study_time = Column(Integer)

    __table_args__ = (
        UniqueConstraint('name', 'type'),
    )
