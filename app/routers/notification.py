from datetime import datetime
from typing import Optional

import boto3
from fastapi import APIRouter, Depends

from app.db.crud import get_email_by_id, post_notification, get_notification, change_notification_status
from app.schemas.notification import Notification
from app.schemas.user import UserInDB
from app.services.send_email import send_notification
from app.services.token import get_current_user

db_client = boto3.resource('dynamodb')
user_table = db_client.Table('notifications')

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)


@router.post('/')
async def create_notification(notification: Notification, current_user: UserInDB = Depends(get_current_user)):
    date = str(datetime.now().date())
    user_id = current_user.id
    email = get_email_by_id(user_id)
    if notification.status == 'not decided':
        send_notification(notification.title, notification.description, email)
    post_notification(notification.__dict__, user_id, date)


@router.get('/')
async def get_notifications(fieldId: Optional[int] = None,
                            status: Optional[str] = None,
                            dateStart: Optional[str] = None,
                            dateEnd: Optional[str] = None, current_user: UserInDB = Depends(get_current_user)
                            ):

    user_id = current_user.id
    response = get_notification(user_id)
    if fieldId is not None:
        response = [note for note in response if note['fieldId'] == fieldId]

    if status is not None:
        response = [note for note in response if note['status'] == status]

    if dateStart is not None:
        response = [note for note in response if note['date'] >= dateStart]

    if dateEnd is not None:
        response = [note for note in response if note['date'] <= dateEnd]

    return {'notifications': response}


@router.put('/{id}/status')
async def change_status(id: str, status: str, current_user: UserInDB = Depends(get_current_user)):
    change_notification_status(id, status)
