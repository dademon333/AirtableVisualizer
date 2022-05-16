from pydantic import BaseModel


class DbElementUpdateCreate(BaseModel):
    column: str
    old_value: str | None
    new_value: str | None
    change_id: int


class DbElementUpdateUpdate(BaseModel):
    pass


class DbElementUpdateInfo(BaseModel):
    column: str
    old_value: str | None
    new_value: str | None

    class Config:
        orm_mode = True
