from sqlalchemy import Integer, Column, Text, String
from sqlalchemy.orm import relationship

from .base import Base


class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    url = Column(Text)
    description = Column(Text)

    attachments = relationship('Attachment', backref='source', lazy='joined')
