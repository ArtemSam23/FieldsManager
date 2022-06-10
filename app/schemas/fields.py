from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal


class FieldInfo(BaseModel):
    name: str
    culture: str


class Geometry(BaseModel):
    type: str
    coordinates: List[List[List[Decimal]]]


class Feature(BaseModel):
    type: str
    geometry: Geometry
    properties: FieldInfo

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {"example": {"type": "Feature",
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
                                    }}


class Field(FieldInfo):
    user_id: Optional[str] = None
    id: str
    problemsCount: int = 0
    geojson: Feature


class GeoJson(BaseModel):
    geoJson: Feature


# class Src(BaseModel):
#     type: str
#     properties: dict["name": str]
#
#
# class FeatureCollection(BaseModel):
#     type: str
#     name: str
#     src: Src
#     features: List[Feature]

