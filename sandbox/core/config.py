from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Load from .env file if it exists
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    def datetime_now(self):
        return datetime.now(tz=pytz.UTC)

    def one_month_datetime(self):
        return datetime.now(tz=pytz.UTC) + relativedelta(months=1)

    def create_dir(self,*name):
        """For creating recursive and non-recursive directories ."""
        fullpath = os.path.join(BASE_DIR, *name)
        os.makedirs(fullpath, exist_ok=True)
        return fullpath


settings = Settings()
