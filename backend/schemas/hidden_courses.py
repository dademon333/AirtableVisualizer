from pydantic import BaseModel


class HiddenCourseCreate(BaseModel):
    course_id: int


class HiddenCourseUpdate(BaseModel):
    pass


class HiddenCourseInfo(BaseModel):
    course_id: int

    class Config:
        orm_mode = True
