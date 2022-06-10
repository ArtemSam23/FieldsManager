from pydantic import BaseModel
from enum import Enum
from typing import Optional


class DocType(str, Enum):
    nda = 'nda'
    agreement = 'agreement'
    ownership = 'ownership'
    card = 'card'
    attachment = 'attachment'


class Document(BaseModel):
    file_name: str
    type: DocType = DocType.attachment
    comment: Optional[str] = None
    # created: str = lambda: str(datetime.now().date())
    status: Optional[str] = False
    dateEnd: Optional[str] = None
    dateStart: Optional[str] = None

    class Config:
        use_enum_values = True
