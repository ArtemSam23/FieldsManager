from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette import status
from app.db.crud import get_user_by_email, update_password_db
from app.services.hash import verify_password
from app.schemas.user import UserInDB
from app.services.send_email import send_code
from app.services.token import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_token, get_token_data,
    Token, EmailTokenData, JWTError
)


from app.routers import registration
router = APIRouter(
    prefix="/auth",
)
router.include_router(registration.router)


def authenticate_user(email: str, password: str):
    current_user = UserInDB(**get_user_by_email(email))
    if not current_user:
        return False
    if not verify_password(password, current_user.hashed_password):
        return False
    return current_user


@router.post("/login", response_model=Token, tags=["auth"])
def login_for_access_token(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_token(data={"sub": user.id}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/restore", tags=["restore"])
async def restore_password(email: EmailStr):
    user = get_user_by_email(email)
    if user:
        user = UserInDB(**user)
        code = registration.random_code()
        send_code(email, code)
        token = create_token({"id": user.id, "email": email, "code": code}, expires_delta=30)
        return {"token": token}
    else:
        raise HTTPException(status_code=400, detail="No user with this email")


@router.post("/restore/confirm", tags=["restore"])
async def confirm_restore_password(code: str, token: str = Header(None)):
    try:
        print(token)
        token_data = get_token_data(token)
        print(token_data)
        if token_data is None:
            raise HTTPException(status_code=400, detail="Could not get token data")

        token_data = EmailTokenData(**token_data)
        if token_data.code != code:
            raise HTTPException(status_code=400, detail="Wrong code")

        pass_token = create_token({"id": token_data.id}, expires_delta=30)
        return {"passToken": pass_token}

    except JWTError:
        raise HTTPException(status_code=400, detail="Could not validate token")


@router.post("/restore/confirm/new", tags=["restore"])
async def change_password(new_password: str, token: str = Header(None)):
    token_data = get_token_data(token)
    user_id = token_data["id"]
    update_password_db(user_id, new_password)
