from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN: str
    DATABASE_URL: str

    class Config(SettingsConfigDict):
        env_file = ".env"

settings = Settings()



def get_database_url():
    return settings.DATABASE_URL

def get_tg_token():
    return settings.TOKEN