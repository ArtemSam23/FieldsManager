from typing import Optional, List

from pydantic import BaseModel, EmailStr, Extra

from app.schemas.documents import Document


class UserBase(BaseModel):
    id: Optional[str] = None
    name: str
    surname: str
    email: EmailStr
    organisation: Optional[str] = None
    disable: bool = True
    docs: List[Document] = []
    fields: Optional[List] = []
    problems: Optional[List] = []

    class Config:
        extra = Extra.ignore

        
class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    organisation: Optional[str] = None
    password: str


class UserInDB(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    name:  Optional[str] = None
    surname:  Optional[str] = None
    email:  Optional[EmailStr] = None
    organisation: Optional[str] = None
