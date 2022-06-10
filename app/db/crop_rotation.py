from operator import attrgetter
from app.db.crud import db_client
from app.schemas.crop_rotation import YearRotation, CropRotation
from typing import Optional


crop_rotation_table = db_client.Table('crop_rotation')


def __get_db_item__(field_id: str) -> Optional[dict]:
    try:
        return crop_rotation_table.get_item(Key={'field_id': field_id})['Item']
    except KeyError:
        return None


def __put_db_item__(crop_rotation: CropRotation):
    return crop_rotation_table.put_item(Item=crop_rotation.dict())


def create_crop_rotation(field_id: str, year_rotation: YearRotation):
    rotation_in_db = __get_db_item__(field_id)
    if rotation_in_db:
        crop_rotation = CropRotation(**rotation_in_db)
        crop_rotation.cropRotation.append(year_rotation)
        crop_rotation.cropRotation.sort(key=attrgetter('year'))
        return __put_db_item__(crop_rotation)
    return __put_db_item__(CropRotation(field_id=field_id, cropRotation=[year_rotation.dict()]))


def get_crop_rotation(field_id: str) -> Optional[CropRotation]:
    crop_rotation = __get_db_item__(field_id)
    if crop_rotation is not None:
        return CropRotation(**__get_db_item__(field_id))
    return None


def get_year_rotation(field_id: str, crop_id: str) -> YearRotation:
    crop_rotation: CropRotation = get_crop_rotation(field_id)
    for year_rotation in crop_rotation.cropRotation:
        if year_rotation.id == crop_id:
            return year_rotation


def update_year_rotation(field_id: str, updated_rotation: YearRotation):
    crop_rotation: CropRotation = get_crop_rotation(field_id)
    crop_rotation.cropRotation.remove(get_year_rotation(field_id, updated_rotation.id))
    crop_rotation.cropRotation.append(updated_rotation)
    crop_rotation.cropRotation.sort(key=attrgetter('year'))
    return __put_db_item__(crop_rotation)


def delete_year_rotation(field_id: str, crop_id: str):
    crop_rotation: CropRotation = get_crop_rotation(field_id)
    rotation_to_delete = get_year_rotation(field_id, crop_id)
    crop_rotation.cropRotation.remove(rotation_to_delete)
    return __put_db_item__(crop_rotation)


def __test1__():
    from pprint import pprint
    crop_id = "test"
    field_id = "5f83c9d1-7a7c-4c68-ba63-2330383ea37b"
    year_rotation = YearRotation(
        id=crop_id,
        year=2026,
        culture="potatoes",
        productivity=1.0,
        area=200.1
    )
    updated_rotation = YearRotation(
        id=crop_id,
        year=2022,
        culture="potatoes",
        productivity=0.87,
        area=200.1
    )

    create_crop_rotation(field_id, year_rotation)
    print()
    pprint(get_crop_rotation(field_id).dict())
    print()
    pprint(get_year_rotation(field_id, crop_id))
    print()
    update_year_rotation(field_id, updated_rotation)
    print()
    pprint(get_year_rotation(field_id, crop_id))
    print()
    delete_year_rotation(field_id, crop_id)
    print()
    pprint(get_crop_rotation(field_id).dict())
    print()


def __test2__():
    from pprint import pprint
    cr = YearRotation(
        year=2026,
        culture="potatoes",
        productivity=1.0,
        area=200.1
    )
    pprint(cr.dict())


if __name__ == '__main__':
    __test2__()
