from fastapi import HTTPException, status
from pydantic import BaseModel


class NotACourseResponse(BaseModel):
    detail: str = 'This entity is not a course'


class CourseNotFoundResponse(BaseModel):
    detail: str = 'Course not found'


class NotACourseError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NotACourseResponse().detail,
        )


class CourseNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CourseNotFoundResponse().detail,
        )
