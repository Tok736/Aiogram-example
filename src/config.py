from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    PYTHONPATH: str

    BOT_TOKEN:  SecretStr

    DB_USER: SecretStr
    DB_PASS: SecretStr
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

env_config = EnvConfig()
