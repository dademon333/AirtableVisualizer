from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

from infrastructure.db.base import Base


class EntityConnection(Base):
    __tablename__ = 'entity_connections'

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
    type_connection_id = Column(
        Integer,
        ForeignKey(
            'entity_type_connections.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        nullable=False,
        index=True
    )

    __table_args__ = (
        UniqueConstraint('parent_id', 'child_id'),
    )
