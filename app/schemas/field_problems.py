from pydantic import BaseModel
from enum import Enum
from uuid import uuid4
from typing import Optional, List


class ProblemTypes(str, Enum):
    no_type = 'no type'
    fire = 'fire'


class Problem(BaseModel):
    fieldsId: List[str] = []
    type: Optional[ProblemTypes] = ProblemTypes.no_type
    title: str = "no title"
    description: str = "no description"

    class Config:
        use_enum_values = True


class ProblemCreate(Problem):
    id: str = str(uuid4())
