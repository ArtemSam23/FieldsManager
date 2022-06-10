from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from geojson import Polygon
from uuid import uuid4
from app.schemas.fields import Feature


class Illness(BaseModel):
    
    name: Optional[str] = None
    period_start: Optional[str] = None
    period_end: Optional[str] = None

    reason: Optional[str] = None
    method_liquidation: Optional[str] = None
    geoJson: Optional[Feature] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        schema_extra = {"example":
                            {"name": "string",
                             "period_start": "string",
                             "period_end": "string",
                             "reason": "string",
                             "method_liquidation": "string",

                             "geoJson": {
                                 "type": "Feature",
                                 "geometry": {
                                     "type": "Polygon",
                                     "coordinates": [

                                         [

                                             [
                                                 40.30776500701904,
                                                 45.62160163372955
                                             ],
                                             [
                                                 40.30755043029785,
                                                 45.61421752374221
                                             ],
                                             [
                                                 40.31587600708008,
                                                 45.61421752374221
                                             ],
                                             [
                                                 40.314674377441406,
                                                 45.621481574677574
                                             ],
                                             [
                                                 40.30776500701904,
                                                 45.62160163372955
                                             ]

                                         ]

                                     ]
                                 },
                                 "properties": {
                                     "name": "name",
                                     "culture": "culture"
                                 }
                             }}}


class IllnessInDB(Illness):
    id: str


class IllnessesInDB(BaseModel):
    field_id: str
    illness_list: list[IllnessInDB] = []



