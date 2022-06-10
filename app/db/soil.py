import boto3
from app.schemas.soil import Soil, SoilInDB
from fastapi import FastAPI, File, UploadFile, HTTPException
from app.s3.actions import create_url, upload_file_to_bucket
db_client = boto3.resource('dynamodb')
soil_table = db_client.Table('soil')


def get_soil_db(field_id: str):
    try:
        soil_dict = soil_table.get_item(Key={"field_id": field_id})['Item']
        del soil_dict['field_id']
        del soil_dict['document']
        return Soil(**soil_dict)
    except:
        raise HTTPException(status_code=404, detail="Item not found")


def get_soilInDB(field_id: str):
    try:
        soil_dict = soil_table.get_item(Key={"field_id": field_id})['Item']

        soil = SoilInDB(**soil_dict)
        return soil
    except:
        raise HTTPException(status_code=404, detail="Item not found")


def create_soil_db(fieldId: str, soil: Soil):
    soil_dict = soil.dict()
    soil_dict['field_id'] = fieldId
    soil_in_db = SoilInDB(**soil_dict)
    soil_table.put_item(Item=soil_in_db.dict())


def create_soil_document(field_id: str, user_id: str, file: UploadFile):
    file_name = upload_file_to_bucket(file, 'backend.documents', 'chemical_analysis', user_id)
    if not file_name:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")
    else:
        soil = get_soilInDB(field_id).dict()
        soil['document'] = file_name
        soil_table.put_item(Item=soil)


def get_soil_document(field_id: str):
    soil = get_soilInDB(field_id)
    soil = soil.dict()
    file_name = soil['document']
    if file_name is not None:
        url = create_url(file_name, expire_in=1000)
        return url
    return file_name


def update_soil_db(field_id:  str, new_soil: Soil):

    old_soil = get_soilInDB(field_id).dict()
    for key, value in new_soil.dict().items():
        if value is not None:
            old_soil[key] = value

    soil_table.put_item(Item=old_soil)
    del old_soil['document']
    del old_soil['field_id']
    return old_soil
