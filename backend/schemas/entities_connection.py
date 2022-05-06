from pydantic import BaseModel


class EntitiesConnectionBase(BaseModel):
    parent_id: int
    child_id: int
    types_connection_id: int


class EntitiesConnectionCreate(EntitiesConnectionBase):
    pass


class EntitiesConnectionUpdate(BaseModel):
    parent_id: int | None = None
    child_id: int | None = None
    types_connection_id: int | None = None


class EntitiesConnectionInfo(EntitiesConnectionBase):
    pass
