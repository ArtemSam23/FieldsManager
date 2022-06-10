from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.db.crud import update_password_db, update_user
from app.schemas.user import UserBase, UserUpdate, UserInDB
from app.services.hash import verify_password
from app.services.token import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/info", response_model=UserUpdate)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user.dict()


@router.put("/password")
async def update_password(password: str, new_password: str, current_user: UserInDB = Depends(get_current_user)):
    user_id = current_user.id
    old_password = current_user.hashed_password
    if verify_password(password, old_password):
        update_password_db(user_id, new_password)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/info")
async def update_users(update_user_info: UserUpdate, current_user: UserInDB = Depends(get_current_user)):
    return update_user(current_user.id, update_user_info.dict(exclude_unset=True))
