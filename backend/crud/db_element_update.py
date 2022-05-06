from db import DbElementUpdate
from schemas.db_element_update import DbElementUpdateCreate, DbElementUpdateUpdate
from .base import CRUDBase


class CRUDDbElementUpdate(CRUDBase[DbElementUpdate, DbElementUpdateCreate, DbElementUpdateUpdate]):
    pass


db_element_update = CRUDDbElementUpdate(DbElementUpdate)
