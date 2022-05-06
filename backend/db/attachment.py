from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True)
    disk_filename = Column(String, nullable=False)
    source_filename = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    source_id = Column(
        Integer,
        ForeignKey('sources.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
