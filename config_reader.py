from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file="C:\Users\maks0\OneDrive\Документы\.env", env_file_encoding='utf-8')

config = Settings()