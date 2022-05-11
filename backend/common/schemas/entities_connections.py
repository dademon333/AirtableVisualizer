from pydantic import BaseModel


class EntitiesConnectionBase(BaseModel):
    parent_id: int
    child_id: int


class EntitiesConnectionBaseExtended(EntitiesConnectionBase):
    types_connection_id: int


class EntitiesConnectionCreate(EntitiesConnectionBaseExtended):
    pass


class EntitiesConnectionUpdate(BaseModel):
    pass


class EntitiesConnectionInfo(EntitiesConnectionBaseExtended):
    class Config:
        orm_mode = True


class EntitiesConnectionInfoReduced(EntitiesConnectionBase):
    class Config:
        orm_mode = True
