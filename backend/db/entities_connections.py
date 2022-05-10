from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

from .base import Base


class EntitiesConnection(Base):
    __tablename__ = 'entities_connections'

    id = Column(Integer, primary_key=True)
    parent_id = Column(
        Integer,
        ForeignKey('entities.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )
    child_id = Column(
        Integer,
        ForeignKey('entities.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    types_connection_id = Column(
        Integer,
        ForeignKey('entities_types_connections.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    __table_args__ = (
        UniqueConstraint('parent_id', 'child_id'),
    )
