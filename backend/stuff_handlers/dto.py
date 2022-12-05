from pydantic import BaseModel


class HostnameOutputDTO(BaseModel):
    hostname: str
