from typing import Optional
from pydantic import BaseModel


class Notification(BaseModel):

    id: Optional[str] = None
    fieldId: int
    title: str
    description: str
    status: str


class NotificationInDB(Notification):

    user_id: str
