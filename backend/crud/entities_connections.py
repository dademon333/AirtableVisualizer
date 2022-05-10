from db import EntitiesConnection
from schemas.entities_connections import EntitiesConnectionCreate, EntitiesConnectionUpdate
from .base import CRUDBase


class CRUDEntitiesConnections(CRUDBase[EntitiesConnection, EntitiesConnectionCreate, EntitiesConnectionUpdate]):
    pass


entities_connections = CRUDEntitiesConnections(EntitiesConnection)
