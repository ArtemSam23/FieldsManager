import time
import requests
import json
from fastapi import APIRouter, Depends, Path, Query
from app.services.token import get_current_user
from app.db.crud import get_field_geojson
from app.services.geojson import convert_geojson, decimal_default


router = APIRouter(
    prefix="/monitoring",
    tags=["monitoring"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/{fieldId}/")
async def call_ml_service(method: str = Query(...), field_id: str = Path(..., alias='fieldId')):
    geojson = get_field_geojson(field_id)
    converted_geojson = convert_geojson(geojson, field_id)
    body = {"method": method,
            "date": ['2020-07-29'],
            "relevance": "earliest",
            "geo_json_dict": converted_geojson}

    url = "http://34.220.165.10/"
    response = requests.post(url, data=json.dumps(body, default=decimal_default))
    return response.json()



if __name__ == '__main__':
    geojson_dict = {
        "type": "FeatureCollection",
        "name": "st",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": [
            {"type": "Feature", "properties": {"Id": 0}, "geometry": {"type": "MultiPolygon", "coordinates": [[[[
                38.297675160392657,
                45.09147095910339],
                [
                    38.297757648374272,
                    45.09145192341532],
                [
                    38.297751303145048,
                    45.091337709286847],
                [
                    38.297732267456979,
                    45.090252675068314],
                [
                    38.297656124704815,
                    45.09022729415085],
                [
                    38.297554601035131,
                    45.088272963511486],
                [
                    38.297459422594898,
                    45.088133368465719],
                [
                    38.295619306083836,
                    45.088120678007101],
                [
                    38.29547971103807,
                    45.088107987548483],
                [
                    38.295422603973975,
                    45.088476010850627],
                [
                    38.295428949203369,
                    45.089059771950701],
                [
                    38.295403568285906,
                    45.089396069106158],
                [
                    38.295327425533685,
                    45.089516628463855],
                [
                    38.294813461956437,
                    45.089510283234461],
                [
                    38.29476270012168,
                    45.090201913233557],
                [
                    38.294470819571529,
                    45.090544555618237],
                [
                    38.294432748195447,
                    45.091496340020683],
                [
                    38.297675160392657,
                    45.09147095910339]]]]}}
        ]
    }
    call_ml_service(geojson_dict)
