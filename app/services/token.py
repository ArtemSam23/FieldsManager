"""
If you want some request to be with token auth import get_current_user app.services.token
and add this to your path func: current_user=Depends(get_current_user)
"""
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.schemas.user import UserInDB
from app.db.crud import get_user

import os
SECRET_KEY = '8iKHVzgusdhNEG+RQOfuXHq1TdDCA9aD8JQvXijh' #os.environ['SECRET_TOKEN_KEY']
ALGORITHM = 'HS256' #os.environ['TOKEN_ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")


# Maybe we should move token models to schemes???
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


class EmailTokenData(BaseModel):
    id: str
    email: EmailStr
    code: str


def create_token(data: dict, expires_delta: Optional[int] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_token_data(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = get_user(user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return UserInDB(**user)
