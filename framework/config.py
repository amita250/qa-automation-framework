from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QA_", env_file=".env")

    base_url: str = "https://restful-booker.herokuapp.com"
    username: str = "admin"
    password: str = "password123"
    timeout: int = 15


settings = Settings()