from decimal import Decimal


def convert_geojson(geojson, field_id):
    new_geojson = {
        "type": "FeatureCollection",
        "name": "st",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": [
            {"type": "Feature", "properties": {"Id": field_id, "culture": geojson["properties"]["culture"],
                                               "name": geojson["properties"]["name"]},
             "geometry": {"type": "MultiPolygon", "coordinates": [[geojson["geometry"]["coordinates"][0]]]}}
        ]
    }
    return new_geojson


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    return str(obj)


'''


geo= {
  "geometry": {
   "coordinates": [
    [
     [
      72.30776500701904,
      98.62160163372955
     ],
     [
      72.30755043029785,
      98.61421752374221
     ],
     [
      72.31587600708008,
      98.61421752374221
     ],
     [
      72.3146743774414,
      98.62148157467757
     ],
     [
      72.30776500701904,
      98.62160163372955
     ]
    ]
   ],
   "type": "Polygon"
  },
  "properties": {
   "culture": "culture",
   "name": "name"
  },
  "type": "Feature"
 }




print(convert_geojson(geo, "fa9a6d78-aced-4912-b7ca-4b1583e0b5fe"))'''
