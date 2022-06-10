from uuid import uuid4
from fastapi import APIRouter, HTTPException, Header, Request
from jose import JWTError
from app.schemas.user import UserCreate, UserInDB
from app.db import crud
from app.services.token import EmailTokenData, create_token, get_token_data
from app.services.send_email import send_code, send_signup_confirmation
from random import randint

router = APIRouter(
    prefix="/registration",
    tags=["registration"],
)


def random_code():
    return hex(randint(10**9, 10**10)).upper()[2:]


@router.post("/")
async def sign_up(user: UserCreate):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    code = random_code()
    new_user_id = str(uuid4())
    send_code(email=user.email, code=code)
    token_data = EmailTokenData(id=new_user_id, email=user.email, code=code)
    token = create_token(data=token_data.dict(), expires_delta=60)
    crud.create_user(user.dict(), user_id=new_user_id)
    return {"token": token}


@router.post("/confirm")
def confirm_email(code: str, token: str = Header(None)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate email token")
    try:
        token_data = get_token_data(token)
        if token_data is None:
            raise credentials_exception
        token_data = EmailTokenData(**token_data)
        user = UserInDB(**crud.get_user(user_id=token_data.id))
        if token_data.code != code:
            raise credentials_exception
        else:
            crud.confirm_email_by_id(user.id)
            send_signup_confirmation(token_data.email)
            return {"message": "email confirmed"}
    except JWTError:
        raise credentials_exception
