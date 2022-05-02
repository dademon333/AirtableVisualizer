from pydantic import BaseModel


class OkResponse(BaseModel):
    response: str = 'ok'
