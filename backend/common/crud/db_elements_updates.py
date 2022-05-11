from common.db import DbElementUpdate
from common.schemas.db_elements_updates import DbElementUpdateCreate, DbElementUpdateUpdate
from .base import CRUDBase


class CRUDDbElementsUpdates(CRUDBase[DbElementUpdate, DbElementUpdateCreate, DbElementUpdateUpdate]):
    pass


db_elements_updates = CRUDDbElementsUpdates(DbElementUpdate)
