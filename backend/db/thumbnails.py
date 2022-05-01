import enum

from sqlalchemy import String, Integer, Column, ForeignKey, Enum, UniqueConstraint

from .base import Base, get_enum_values


class ThumbnailSize(str, enum.Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'


class Thumbnail(Base):
    __tablename__ = 'thumbnails'

    id = Column(Integer, primary_key=True)
    disk_filename = Column(String, nullable=False)
    size = Column(
        Enum(ThumbnailSize, name='thumbnail_size', values_callable=get_enum_values),
        nullable=False
    )
    height = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    attachment_id = Column(
        Integer,
        ForeignKey('attachments.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    __table_args__ = (
        UniqueConstraint('attachment_id', 'size'),
    )
