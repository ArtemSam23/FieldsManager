from fastapi import APIRouter, Depends, Path, status
from app.services.token import get_current_user
from app.schemas.user import UserInDB
from app.schemas.fields import Field, FieldInfo, GeoJson
from app.schemas.crop_rotation import YearRotation, CropRotation, YearRotationIn
from app.db.crud import create_field, update_field, update_polygon, update_user, get_field, delete_field_db
from app.db.crop_rotation import create_crop_rotation, get_crop_rotation, update_year_rotation, delete_year_rotation
import json
from decimal import *
from uuid import uuid4
from app.schemas.chemicals import Chemical, ChemicalBase
from app.schemas.illnesses import Illness
from app.db.chemical_treatment import create_treatment, update_treatment, get_all_treatments, del_treatment
from app.db.illnesses import create_illness, get_illnesses, delete_illnesses, update_illnesses
from app.db.soil import create_soil_db, get_soil_db, create_soil_document, get_soil_document, update_soil_db
from app.schemas.soil import Soil
from app.schemas.vegetation import VegetationBase, Vegetation
from app.db.vegetation import add_vegetation, get_all_vegetation, update_vegetation, del_vegetation
from fastapi import File, UploadFile

router = APIRouter(
    prefix="/fields",
    tags=["fields"],
    dependencies=[Depends(get_current_user)]
)


@router.post('/')
async def post_field(field: GeoJson, current_user: UserInDB = Depends(get_current_user)):
    field = field.geoJson
    id_field = str(uuid4())
    new_field = Field(id=id_field,
                      user_id=current_user.id,
                      name=field.properties.name,
                      culture=field.properties.culture,
                      geojson=field)
    create_field(new_field)
    current_user.fields.append(id_field)
    update_user(current_user.id, current_user.dict())

    return {'name': new_field.name, 'culture': new_field.culture}


@router.put('/{id}')
async def put_field_info(field_info: FieldInfo, field_id: str = Path(..., alias='id')):
    update_field(field_id, field_info.name, field_info.culture)


@router.put('/{id}/polygon')
async def put_field_polygon(field: GeoJson, field_id: str = Path(..., alias='id')):
    field = field.geoJson
    new_polygon = field.geometry.coordinates[0]

    update_polygon(field_id, new_polygon)


@router.post('/{fieldId}/crop-rotation', response_model=YearRotation)
async def new_crop_rotation(year_rotation: YearRotationIn, field_id=Path(..., alias='fieldId')):
    year_rotation = YearRotation(**year_rotation.dict())
    create_crop_rotation(field_id, year_rotation)
    return year_rotation


@router.get('{fieldId}/crop-rotation', response_model=CropRotation, response_model_exclude={'field_id'})
async def get_rotation(field_id: str = Path(..., alias='fieldId')):
    crop_rotation = get_crop_rotation(field_id)
    if crop_rotation:
        return crop_rotation
    return {"cropRotation": [], "field_id": field_id}


@router.put('/{fieldId}/crop-rotation/{cropId}', response_model=YearRotation)
async def update_rotation(
        updated_rotation: YearRotationIn,
        field_id: str = Path(..., alias='fieldId'),
        crop_id: str = Path(..., alias='cropId')):
    updated_rotation = YearRotation(id=crop_id, **updated_rotation.dict())
    update_year_rotation(field_id, updated_rotation)
    return updated_rotation


@router.delete('{fieldId}/crop-rotation/{cropId}', status_code=status.HTTP_200_OK)
async def remove_year_rotation(field_id: str = Path(..., alias='fieldId'), crop_id: str = Path(..., alias='cropId')):
    response = delete_year_rotation(field_id, crop_id)
    print(response)


@router.post('/{fieldId}/chemical-treatment')
async def post_chemical_treatment(new_chemical_treatment: ChemicalBase,
                                  field_id: str = Path(..., alias='fieldId')):
    chemical_treatment = Chemical(**new_chemical_treatment.dict())
    create_treatment(field_id, chemical_treatment)
    return chemical_treatment


@router.get('{fieldId}/chemical-treatment')
async def get_chemical_treatments(field_id: str = Path(..., alias='fieldId')):
    chemical_treatment = get_all_treatments(field_id)
    if chemical_treatment:
        return chemical_treatment
    return {"chemicalTreatment": [], "field_id": field_id}


@router.put('/{fieldId}/chemical-treatment/{treatmentId}')
async def put_chemical_treatment(new_chemical_treatment: ChemicalBase,
                                 field_id: str = Path(..., alias='fieldId'),
                                 treatment_id: str = Path(..., alias='treatmentId')):
    updated_treatment = Chemical(id=treatment_id, **new_chemical_treatment.dict())
    update_treatment(field_id, updated_treatment)
    return updated_treatment


@router.delete('{fieldId}/chemical-treatment/{treatmentId}', status_code=status.HTTP_200_OK)
async def delete_chemical_treatment(field_id: str = Path(..., alias='fieldId'),
                                    treatment_id: str = Path(..., alias='treatmentId')):
    return del_treatment(field_id, treatment_id)


@router.get('/')
async def get_fields(current_user: UserInDB = Depends(get_current_user)):
    fields_id = current_user.fields
    fields_list = [get_field(field_id).dict() for field_id in fields_id]
    return {'fields': fields_list}


@router.delete('/{id}')
async def delete_field(field_id: str = Path(..., alias='id'), current_user: UserInDB = Depends(get_current_user)):
    current_user.fields.remove(field_id)
    update_user(current_user.id, {'fields': current_user.dict()['fields']})
    delete_field_db(field_id)


@router.post('/{fieldId}/diseases')
async def post_illness(illness: Illness, field_id: str = Path(..., alias='fieldId'),
                       current_user: UserInDB = Depends(get_current_user)):
    if current_user:
        create_illness(field_id, illness)


@router.get('/{fieldId}/diseases')
async def get_illness(field_id: str = Path(..., alias='fieldId'), current_user: UserInDB = Depends(get_current_user)):
    if current_user:
        response = get_illnesses(field_id)
        if type(response) is not dict:
            return {'illnesses': response.dict()['illness_list']}
        else:
            return response


@router.delete('/{fieldId}/diseases/{diseaseId}')
async def delete_illness(field_id: str = Path(..., alias='fieldId'), disease_id: str = Path(..., alias='diseaseId'),
                         current_user: UserInDB = Depends(get_current_user)):
    if current_user:
        delete_illnesses(field_id, disease_id)


@router.put('/{fieldId}/diseases/{diseaseId}')
async def update_illness(illness: Illness, field_id: str = Path(..., alias='fieldId'),
                         disease_id: str = Path(..., alias='diseaseId'),
                         current_user: UserInDB = Depends(get_current_user)):
    if current_user:
        response = update_illnesses(field_id, disease_id, illness)
        return response


@router.post('/{fieldId}/soil')
async def create_soil(soil: Soil, field_id: str = Path(..., alias='fieldId'),
                      current_user: UserInDB = Depends(get_current_user)):
    if current_user:
        create_soil_db(field_id, soil)
        return soil


@router.put('/{fieldId}/soil')
async def update_soil(soil: Soil, field_id: str = Path(..., alias='fieldId'),
                      current_user: UserInDB = Depends(get_current_user)):
    if current_user:
        new_soil = update_soil_db(field_id, soil)
        return new_soil


@router.get('/{fieldId}/soil')
async def get_soil(field_id: str = Path(..., alias='fieldId')):
    response = get_soil_db(field_id)
    if type(response) is not dict:
        response = response.dict()
    return response


@router.put('/{fieldId}/soil/docs')
async def update_soil_doc(field_id: str = Path(..., alias='fieldId'), file: UploadFile = File(...),
                          current_user: UserInDB = Depends(get_current_user)):
    if current_user:
        create_soil_document(field_id, current_user.id, file)


@router.get('/{fieldId}/soil/docs')
async def get_soil_doc(field_id: str = Path(..., alias='fieldId')):
    doc_url = get_soil_document(field_id)
    return {'url': doc_url}


@router.post('/{fieldId}/vegetation')
async def post_vegetation(new_vegetation: VegetationBase,
                          field_id: str = Path(..., alias='fieldId')):
    vegetation = Vegetation(**new_vegetation.dict())
    add_vegetation(field_id, vegetation)
    return vegetation


@router.get('/{fieldId}/vegetation')
async def get_vegetation(field_id: str = Path(..., alias='fieldId')):
    all_vegetation = get_all_vegetation(field_id)
    if all_vegetation:
        return all_vegetation
    return {"Vegetation": [], "field_id": field_id}


@router.put('/{fieldId}/vegetation/{vegetationId}')
async def put_vegetation(vegetation_base: VegetationBase,
                         field_id: str = Path(..., alias='fieldId'),
                         vegetation_id: str = Path(..., alias='vegetationId')):
    vegetation = Vegetation(id=vegetation_id, **vegetation_base.dict())
    update_vegetation(field_id, vegetation)
    return vegetation


@router.delete('/{fieldId}/vegetation/{vegetationId}', status_code=status.HTTP_200_OK)
async def delete_vegetation(field_id: str = Path(..., alias='fieldId'),
                            vegetation_id: str = Path(..., alias='vegetationId')):
    return del_vegetation(field_id, vegetation_id)
