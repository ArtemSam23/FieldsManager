from pydantic import BaseModel
from typing import Optional


class Soil(BaseModel):

    type: Optional[str] = None
    erosion: Optional[str] = None
    ph: Optional[str] = None
    magnesiumContent: Optional[str] = None
    potassiumContent: Optional[str] = None
    nitrogenContent: Optional[str] = None
    chemicalLastDay: Optional[str] = None
    fertilizationLastDay: Optional[str] = None
    comment: Optional[str] = None

        
        
class SoilInDB(Soil):
    field_id: str = ''
    document: Optional[str] = None
