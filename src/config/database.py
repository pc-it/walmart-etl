from pathlib import Path
from typing import Optional, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator, ValidationInfo, Field


BASE_DIR = Path(__file__).parent.parent.parent


class DatabaseSettings(BaseSettings):

    model_config = SettingsConfigDict(extra='allow', env_file=BASE_DIR / 'config/.env')

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = Field(default=None, validate_default=True)

    @field_validator('SQLALCHEMY_DATABASE_URI', mode='before')
    def assemble_db_connection(cls, v: Optional[str], validation_info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        values = validation_info.data
        return f'postgresql://{values.get("POSTGRES_USER")}:{values.get("POSTGRES_PASSWORD")}@{values.get("POSTGRES_SERVER")}'
    

database_settings = DatabaseSettings()
