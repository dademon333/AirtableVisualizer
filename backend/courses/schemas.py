from pydantic import BaseModel


class CourseNotFoundResponse(BaseModel):
    detail: str = 'Course not found'


class NotACourseErrorResponse(BaseModel):
    detail: str = 'This entity is not a course'
