from fastapi import Path
from app.db.crud import db_client
from app.schemas.chemicals import ChemicalTreatments, Chemical
from typing import Optional
from datetime import date
from uuid import uuid4

chemical_treatment_table = db_client.Table('chemical_treatment')


def __get_db_item__(field_id: str) -> Optional[dict]:
    try:
        return chemical_treatment_table.get_item(Key={'field_id': field_id})['Item']
    except KeyError:
        return None


def __put_db_item__(chemical_treatment: ChemicalTreatments):
    return chemical_treatment_table.put_item(Item=chemical_treatment.dict())


def create_treatment(field_id: str, new_chemical: Chemical):
    chemical_treatment_db = __get_db_item__(field_id)

    if chemical_treatment_db:
        chemical_treatment = ChemicalTreatments(**chemical_treatment_db)
        chemical_treatment.treatments.append(new_chemical)
        return __put_db_item__(chemical_treatment)

    return __put_db_item__(ChemicalTreatments(field_id=field_id, treatments=[new_chemical.dict()]))


def update_treatment(field_id: str, new_chemical: Chemical):
    chemical_treatments: ChemicalTreatments = get_all_treatments(field_id)
    print(chemical_treatments)
    if chemical_treatments is not None and get_treatment(field_id, new_chemical.id) is not None:
        chemical_treatments.treatments.remove(get_treatment(field_id, new_chemical.id))
    chemical_treatments.treatments.append(new_chemical)
    return __put_db_item__(chemical_treatments)


def get_all_treatments(field_id: str = Path(..., alias='fieldId')) -> Optional[ChemicalTreatments]:
    chemical_treatment = __get_db_item__(field_id)
    if chemical_treatment is not None:
        return ChemicalTreatments(**__get_db_item__(field_id))
    return None


def get_treatment(field_id: str, treatment_id: str) -> Chemical:
    chemical_treatments: ChemicalTreatments = get_all_treatments(field_id)
    for chem_treat in chemical_treatments.treatments:
        if chem_treat.id == treatment_id:
            return chem_treat


def del_treatment(field_id: str, treatment_id: str) -> Optional[ChemicalTreatments]:
    chemical_treatments: ChemicalTreatments = get_all_treatments(field_id)
    deleted_treatment = get_treatment(field_id, treatment_id)
    chemical_treatments.treatments.remove(deleted_treatment)
    return __put_db_item__(chemical_treatments)


if __name__ == '__main__':
    from pprint import pprint

    # put_treatment('1', Chemical(id='5', substance='Water', date='2020-03-12', dose='2.3'))
    id = '1'
    # pprint(__get_db_item__(id))
    #   get_crop_rotation(id)
    # pprint(__get_db_item__(id))
    # pprint(chemical_treatment_table.get_item(Key={'field_id': id}))
