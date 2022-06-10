from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field
from decimal import Decimal
# from datetime import date
from hashlib import md5
from typing import NewType, List

TreatmentId = NewType('Id', str)


class ChemicalBase(BaseModel):
    substance: str
    date: str  # 'YYYY-MM-DD'
    dose: str
    cause: Optional[str] = None
    comment: Optional[str] = None
    method: Optional[str] = None

    '''def __hash__(self):
        return self.fertilizer.encode() + self.date.encode()

    def get_str_hash(self):
        return md5(self.__hash__()).hexdigest()'''


class Chemical(ChemicalBase):
    id: str = Field(default_factory=lambda: str(uuid4()))


class ChemicalTreatments(BaseModel):
    field_id: str
    treatments: List[Chemical] = []


if __name__ == '__main__':
    from pprint import pprint

    model = Chemical(fertilizer='salt', date="2020-07-14", dose=2.5, comment='-', method='-')
    pprint(model)
    pprint(model.dict())
