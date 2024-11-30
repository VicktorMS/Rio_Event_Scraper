# config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator, computed_field
from pathlib import Path

class Settings(BaseSettings):
    # Configurações Gerais
    app_name: str = Field(default="VictorMoraesPbTP5", env="APP_NAME")
    environment: str = Field(default="DEV", env="ENVIRONMENT")
    target_url: str = Field(default="https://google.com", env="TARGET_URL")
    database_url: str = Field(default="sqlite:///src/data/tp5_data.db", env="DATABASE_URL")
    scraper_log: str = Field(default="src/logs/scraper.log", env="SCRAPER_LOG")
    
    
    @field_validator("environment")
    def validate_environment(cls, v):
        v_upper = v.upper()
        allowed = ("DEV", "TEST", "PROD")
        if v_upper not in allowed:
            raise ValueError("environment must be 'DEV', 'TEST', or 'PROD'")
        return v_upper

    @computed_field
    def database_path(self) -> Path:
        return Path(self.database_url.replace("sqlite:///", ""))
    
    model_config = SettingsConfigDict(
        extra='allow',
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",  
    )

settings = Settings()