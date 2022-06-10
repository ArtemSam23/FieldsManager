from pydantic import BaseModel
from enum import Enum


class SettingTypes(str, Enum):
    monitoring = 'operational_monitoring'
    language = 'language'
    summary = 'summary_period'
    newsletter = 'newsletter'


class Language(str, Enum):
    ru = "ru"
    en = "en"


class OperationalMonitoring(BaseModel):
    fires: bool = False
    gases: bool = False
    ph: bool = False
    soil_temperature: bool = False
    weather: bool = False


class UserSettings(BaseModel):
    id: str

    summary_period: int = 0
    newsletter: bool = False
    language: Language = Language.ru
    operational_monitoring: OperationalMonitoring = OperationalMonitoring()

    class Config:
        use_enum_values = True
