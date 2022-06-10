from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Optional, List


class VegetationBase(BaseModel):
    number: int
    title: str
    description: Optional[str]
    startDate: str
    endDate: str


class Vegetation(VegetationBase):
    id: str = Field(default_factory=lambda: str(uuid4()))


class VegetationStages(BaseModel):
    field_id: str
    vegetation: List[Vegetation] = []
