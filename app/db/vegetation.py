from fastapi import Path
from app.db.crud import db_client
from typing import Optional
from app.schemas.vegetation import Vegetation, VegetationStages

vegetation_table = db_client.Table('vegetation')


def __get_db_item__(field_id: str) -> Optional[dict]:
    try:
        return vegetation_table.get_item(Key={'field_id': field_id})['Item']
    except KeyError:
        return None


def __put_db_item__(vegetation_stages: VegetationStages):
    return vegetation_table.put_item(Item=vegetation_stages.dict())


def add_vegetation(field_id: str, vegetation: Vegetation):
    vegetation_stages_dict = __get_db_item__(field_id)

    if vegetation_stages_dict:
        vegetation_stages = VegetationStages(**vegetation_stages_dict)
        vegetation_stages.vegetation.append(vegetation)
        return __put_db_item__(vegetation_stages)

    return __put_db_item__(VegetationStages(field_id=field_id, vegetation=[vegetation.dict()]))


def update_vegetation(field_id: str, new_vegetation: Vegetation):
    all_vegetation: VegetationStages = get_all_vegetation(field_id)
    updated_vegetation = get_vegetation(field_id, new_vegetation.id)
    if all_vegetation and updated_vegetation:
        all_vegetation.vegetation.remove(updated_vegetation)
    all_vegetation.vegetation.append(new_vegetation)
    return __put_db_item__(all_vegetation)


def get_all_vegetation(field_id: str = Path(..., alias='fieldId')) -> Optional[VegetationStages]:
    vegetation = __get_db_item__(field_id)
    if vegetation is not None:
        return VegetationStages(**vegetation)
    return None


def get_vegetation(field_id: str, vegetation_id: str) -> Optional[Vegetation]:
    all_vegetation: VegetationStages = get_all_vegetation(field_id)
    for vegetation in all_vegetation.vegetation:
        if vegetation.id == vegetation_id:
            return vegetation
    return None


def del_vegetation(field_id: str, vegetation_id: str) -> Optional[VegetationStages]:
    all_vegetation: VegetationStages = get_all_vegetation(field_id)
    deleted_vegetation = get_vegetation(field_id, vegetation_id)
    try:
        all_vegetation.vegetation.remove(deleted_vegetation)
    except ValueError:
        return None
    return __put_db_item__(all_vegetation)
