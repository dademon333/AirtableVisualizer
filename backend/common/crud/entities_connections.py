from common.db import EntitiesConnection
from common.schemas.entities_connections import EntitiesConnectionCreate, EntitiesConnectionUpdate
from .base import CRUDBase


class CRUDEntitiesConnections(CRUDBase[EntitiesConnection, EntitiesConnectionCreate, EntitiesConnectionUpdate]):
    pass


entities_connections = CRUDEntitiesConnections(EntitiesConnection)
