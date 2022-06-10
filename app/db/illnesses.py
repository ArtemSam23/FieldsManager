from typing import Optional, List, Union
from uuid import uuid4
from app.schemas.illnesses import Illness, IllnessesInDB, IllnessInDB
from decimal import *
import boto3
import json
db_client = boto3.resource('dynamodb')
illnesses_table = db_client.Table('illnesses')


def get_illnesses(field_id: str) -> Union[IllnessesInDB, dict]:

    illnesses = illnesses_table.get_item(Key={'field_id': field_id})
    if 'Item' in illnesses:
        illnesses = illnesses['Item']
        return IllnessesInDB(**illnesses)

    else:
        return {"illnesses": []}

    
def create_illness(field_id: str, illness: Illness):
    illnesses_dict = illnesses_table.get_item(Key={'field_id': field_id})
    if 'Item' in illnesses_dict:
        illnesses_list = illnesses_dict['Item']['illness_list']
        illness_dict = illness.dict()
        illness_dict['id'] = str(uuid4())
        illnesses_list.append(illness_dict)
        new_illness = IllnessesInDB(field_id=field_id, illness_list=illnesses_list)
        illnesses_table.put_item(Item=new_illness.dict())
    else:
        first_illness = IllnessesInDB(field_id=field_id, illness_list=[illness.dict()])
        illnesses_table.put_item(Item=first_illness.dict())


def delete_illnesses(field_id: str, disease_id: str):
    illnesses = get_illnesses(field_id)
    illness_list = illnesses.illness_list
    for ill in illness_list:
        if ill.id == disease_id:
            illness_list.remove(ill)

    illnesses.illness_list = illness_list
    illnesses_table.put_item(Item=illnesses.dict())


def update_illnesses(field_id: str, disease_id, new_illness: Illness):
    illnesses = get_illnesses(field_id)
    illness_list = illnesses.illness_list

    response = None

    for ill in illness_list:
        if ill.id == disease_id:
            illness_list.remove(ill)
            ill = ill.dict()
            for key, value in new_illness.dict().items():
                if value is not None:
                    ill[key] = value

            illness_list.append(ill)
            response = ill

    illnesses.illness_list = illness_list
    illnesses_table.put_item(Item=illnesses.dict())
    return response

