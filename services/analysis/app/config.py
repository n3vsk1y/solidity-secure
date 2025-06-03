from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    etherscan_api_key: str
    analysis_timeout: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()