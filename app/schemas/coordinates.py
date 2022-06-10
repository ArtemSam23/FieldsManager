from pydantic import BaseModel


class Coordinates(BaseModel):
    lat: str
    lon: str
