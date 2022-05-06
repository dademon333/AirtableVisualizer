from pydantic import BaseModel


class DbElementUpdateCreate(BaseModel):
    column: str
    old_value: str
    new_value: str
    change_id: int


class DbElementUpdateUpdate(BaseModel):
    pass


class DbElementUpdateInfo(BaseModel):
    column: str
    old_value: str
    new_value: str

    class Config:
        orm_mode = True
