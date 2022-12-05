from sqlalchemy import Integer, Column, String, ForeignKey, Text

from infrastructure.db.base import Base


class DBElementUpdate(Base):
    __tablename__ = 'db_element_updates'

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
