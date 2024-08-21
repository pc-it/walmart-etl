from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent


class WalmartSettings(BaseSettings):
    WALMART_CLIENT_ID: str
    WALMART_CLIENT_SECRET: str
    WALMART_CONSUMER_CHANNEL_TYPE: str
    WALMART_QOS_CORRELATION_ID: str

    class Config:
        env_file = BASE_DIR / 'config/.env'
        extra = 'allow'


walmart_settings = WalmartSettings()
