from db import EntitiesConnection
from schemas.entities_connection import EntitiesConnectionCreate, EntitiesConnectionUpdate
from .base import CRUDBase


class CRUDEntitiesConnection(CRUDBase[EntitiesConnection, EntitiesConnectionCreate, EntitiesConnectionUpdate]):
    pass


entities_connection = CRUDEntitiesConnection(EntitiesConnection)
