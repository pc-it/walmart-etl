from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent


class SlackApiSettings(BaseSettings):

    TOKEN: str = Field(alias='SLACK_TOKEN')
    CHANNEL: str = Field(alias='SLACK_CHANNEL')

    class Config:
        env_file = BASE_DIR / 'config/.env'
        extra = 'allow'


slack_settings = SlackApiSettings()
