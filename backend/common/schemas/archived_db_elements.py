from pydantic import BaseModel


class ArchivedDbElementCreate(BaseModel):
    element_data: dict
    change_id: int


class ArchivedDbElementUpdate(BaseModel):
    pass


class ArchivedDbElementInfo(BaseModel):
    element_data: dict

    class Config:
        orm_mode = True
