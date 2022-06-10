from decimal import Decimal
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import NewType, List


CropId = NewType('Id', str)


class YearRotationIn(BaseModel):
    year: int
    culture: str
    productivity: Decimal
    area: Decimal


class YearRotation(YearRotationIn):
    id: str = Field(default_factory=lambda: str(uuid4()))


class CropRotation(BaseModel):
    field_id: str
    cropRotation: List[YearRotation] = []
