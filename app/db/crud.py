import boto3
from fastapi import HTTPException
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from typing import Optional
from uuid import uuid4

from app.schemas.documents import Document
from app.services.hash import get_password_hash
from app.schemas.settings import UserSettings
from app.schemas.fields import Field
from app.schemas.field_problems import Problem, ProblemCreate

from pprint import pprint
from app.schemas.exceptions import GetItemException

db_client = boto3.resource('dynamodb', region_name='us-west-2', )
user_table = db_client.Table('users')
settings_table = db_client.Table('settings')
notifications_table = db_client.Table('notifications')
problems_table = db_client.Table('problems')
fields_table = db_client.Table('field')


# User
def create_user(user: dict, user_id: Optional[str] = None):
    try:
        if user_id is not None:
            user['id'] = user_id
        else:
            user['id'] = str(uuid4())
        user['hashed_password'] = get_password_hash(password=user['password'])
        del user['password']
        doc_model: list[Document] = []
        user.update(
            {'disable': True, 'docs': doc_model})
        response = user_table.put_item(Item=user)
        return response
    except ClientError as error:
        return {'Error': str(error.response['Error']['Message'])}


def get_user(user_id: str):
    try:
        response = user_table.get_item(Key={'id': user_id})
        return response['Item']
    except ClientError as error:
        return {'Error': str(error.response['Error']['Message'])}


def get_user_by_email(email: str):
    try:
        user = user_table.scan(FilterExpression=Attr('email').contains(email))['Items']
        if user:
            user_id = user[0]['id']
            return get_user(user_id)
        return None
    except ClientError as error:
        return {'Error': str(error.response['Error']['Message'])}


def update_user(user_id: str, updated: dict):
    user = get_user(user_id)
    for key, value in updated.items():
        user[key] = value
    response = user_table.put_item(Item=user)
    return response


def confirm_email_by_id(user_id: str):
    doc_model: list[Document] = []
    field_model: Optional[list] = []
    problem_model: Optional[list] = []
    response = update_user(user_id,
                           {'disable': False,
                            'docs': doc_model,
                            'fields': field_model,
                            'problems': problem_model}
                           )
    user_settings = UserSettings(id=user_id)
    settings_table.put_item(Item=user_settings.dict())
    return response


def update_password_db(user_id: str, new_password: str):
    new_hashed_password = get_password_hash(new_password)
    user = get_user(user_id)
    user['hashed_password'] = new_hashed_password
    response = user_table.put_item(Item=user)
    return response


# User settings
def get_user_settings(user_id: str):
    try:
        return settings_table.get_item(Key={'id': user_id})['Item']
    except ClientError as error:
        return {'Error': str(error.response['Error']['Message'])}


def update_settings(user_id: str, updated: dict):
    user_settings = get_user_settings(user_id)
    for key, value in updated.items():
        user_settings[key] = value
    response = settings_table.put_item(Item=user_settings)
    return response


# Notifications
def get_email_by_id(user_id: str):
    user = get_user(user_id)
    email = user['email']
    return email


def get_notification(user_id: str):
    notifications = notifications_table.scan(FilterExpression=Attr('user_id').contains(user_id))['Items']
    for notification in notifications:
        del notification['user_id']
    return notifications


def post_notification(notification: dict, user_id: str, date: str):
    notification['user_id'] = user_id
    notification['date'] = date
    notification_id = notification['id']
    if notification_id is not None:
        notification['id'] = notification_id
    else:
        notification['id'] = str(uuid4())
    notifications_table.put_item(Item=notification)


def change_notification_status(notification_id: str, status: str):
    notification = notifications_table.get_item(Key={'id': notification_id})
    notification['Item']['status'] = status
    notifications_table.put_item(Item=notification['Item'])


# Field problems
def create_problem(problem: ProblemCreate):
    response = problems_table.put_item(Item=problem.dict())
    return response


def get_problem(problem_id: str) -> Problem:
    try:
        problem_dict = problems_table.get_item(Key={"id": problem_id})['Item']  # TODO: try except
        return Problem(**problem_dict)
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")


# Fields
def create_field(field: Field):

    response = fields_table.put_item(Item=field.dict())
    return response


def update_field(field_id: str, name: str, culture: str):
    try:
        old_field = fields_table.get_item(Key={'id': field_id})['Item']
        old_field['name'] = name
        old_field['culture'] = culture
        new_field = fields_table.put_item(Item=old_field)
        return new_field
    except ClientError as error:
        return {'Error': str(error.response['Error']['Message'])}


"""
For crop rotation in Field db:

def add_crop_rotation(field_id: str, new_crop_rotation: CropRotation):
    field = fields_table.get_item(Key={'id': field_id})['Item']
    try:
        for crop_rotation in field['crop_rotation']:
            if crop_rotation['year'] == new_crop_rotation.year:
                field['crop_rotation'].remove(crop_rotation)
        field['crop_rotation'].append(new_crop_rotation.dict())
        field['crop_rotation'].sort()
    except KeyError:
        field.update({'crop_rotation': [new_crop_rotation.dict()]})
    pprint(field)
    response = fields_table.put_item(Item=field)
    return response
"""


def update_problem_count(field_id: str):
    field = fields_table.get_item(Key={'id': field_id})['Item']
    field['problemsCount'] += 1
    fields_table.put_item(Item=field)


def update_polygon(field_id: str, new_polygon: list):
    old_field = fields_table.get_item(Key={'id': field_id})['Item']
    print(old_field)
    old_field['geojson']['geometry']['coordinates'][0] = new_polygon
    new_field = fields_table.put_item(Item=old_field)
    return new_field


def get_field(field_id: str):
    try:
        field = fields_table.get_item(Key={'id': field_id})['Item']
        return Field(**field)
    except :
        raise HTTPException(status_code=404, detail="Item not found")


def get_field_coordinates(field_id: str):
    field = get_field(field_id).dict()
    coordinates = field["geojson"]['geometry']['coordinates'][0]
    return coordinates


def get_field_geojson(field_id: str):
    field_id = get_field(field_id).dict()
    geojson = field_id["geojson"]
    return geojson


def delete_field_db(field_id: str):
    try:
        fields_table.delete_item(Key={'id': field_id})
    except ClientError as error:
        return {'Error': str(error.response['Error']['Message'])}


if __name__ == '__main__':
    pass
    # Tests for users:
    """
    from app.schemas.user import UserCreate, UserUpdate
    user = UserCreate(
        email='artemsam23@gmail.com',
        name='Artem',
        surname='Sam',
        password='mypassword'
    )
    user_update = UserUpdate(
        id='1f2c2bcd-bb06-4097-9b53-ee4cfdb276b4',
        password='new_password'
    )
    print(update_password_db(user_update.id, user_update.password))
    print(create_user(user.dict()))
    get_user(user_id)
    print(update_user('4944d0fe-7f13-42f3-9e36-53d3cf2bf376', {'email': 'artemsam23@gmail.com'}))
    print(get_user(user_id))
    print(confirm_email_by_id(user_id))
    user_id = get_user_by_email('artemsam23@gmail.com')['id']
    confirm_email_by_id(user_id)
    """

    # Tests for user settings:
    """
    print(get_user_settings(user_id))
    update_settings(user_id=user_id, updated={"language": "en"})
    print(get_user_settings(user_id))
    """

    # Tests for field problems
    """
    problem = ProblemCreate()
    print(problem.dict())
    create_problem(problem)
    problem_id = '48bdea61-b87b-4452-b5b8-bed401919064'
    print(get_problem(problem_id))
    """

    # Test for crop rotation
    """
    FIELD_ID = '6493dcf4-f021-4151-9a62-a6aba7f38826'
    new_crop_rotation = CropRotation(year=2020, culture='tomatoes', area=200, productivity=1)
    add_crop_rotation(FIELD_ID, new_crop_rotation)
    pprint(get_field(FIELD_ID))
    """

    #Test for field coordinates
    '''
    coordinates = get_field_coordinates("5b265908-9593-4c4e-99f3-8b00d81b64cb")
    print(coordinates)
    '''
    print(get_field_geojson("34a06f60-0e16-4c1a-b789-e0c5eb713fa1"))