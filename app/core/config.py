from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER : str = "saul"
    DB_PASSWORD : str = "secret"
    DB_HOST : str = "db"
    DB_PORT : str = "5432"
    DB_NAME : str = "market_data"

    @property
    def database_url(self):
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()