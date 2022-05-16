from sqlalchemy import Integer, Column, String, ForeignKey, Text

from .base import Base


class DbElementUpdate(Base):
    __tablename__ = 'db_elements_updates'

    id = Column(Integer, primary_key=True)
    column = Column(String, nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)

    change_id = Column(
        Integer,
        ForeignKey('change_log.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
