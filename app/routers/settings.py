from fastapi import APIRouter, Depends, Path
from app.schemas.user import UserBase
from app.schemas.settings import OperationalMonitoring, SettingTypes, UserSettings, Language
from app.services.token import get_current_user
from app.db.crud import get_user_settings, update_settings


router = APIRouter(
    prefix="/settings",
    tags=["settings"]
)


async def user_settings(user: UserBase = Depends(get_current_user)):
    dict_settings = get_user_settings(user.id)
    return UserSettings(**dict_settings)


@router.get("/{settingType}")
def get_settings(settings_type: SettingTypes = Path(..., alias="settingType"), settings: UserSettings = Depends(user_settings)):
    if settings_type == SettingTypes.monitoring:
        return settings.dict()[settings_type]
    return settings.dict(include={settings_type})


@router.put("/monitoring")
def update_monitoring(updated_settings: OperationalMonitoring, user: UserBase = Depends(get_current_user)):
    response = update_settings(user.id, {SettingTypes.monitoring: updated_settings.dict()})
    return response


@router.put("/language")
def update_language(language: Language, user: UserBase = Depends(get_current_user)):
    response = update_settings(user.id, {SettingTypes.language: language})
    return response


@router.put("/summary")
def update_summary(summary: int, user: UserBase = Depends(get_current_user)):
    response = update_settings(user.id, {SettingTypes.summary: summary})
    return response


@router.put("/newsletter")
def update_newsletter(newsletter: bool, user: UserBase = Depends(get_current_user)):
    response = update_settings(user.id, {SettingTypes.newsletter: newsletter})
    return response
